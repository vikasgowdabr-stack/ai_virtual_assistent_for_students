from transformers import pipeline
import json
from typing import List, Dict, Optional
import re

class KnowledgeGraph:
    def __init__(self, ner_model="dslim/bert-base-NER", data_path="data/knowledge_graph_data.json"):
        """Initialize the knowledge graph component."""
        try:
            # Force CPU usage to avoid CUDA memory issues
            self.ner_pipe = pipeline("ner", model=ner_model, device=-1)
            print(f"✅ NER model loaded: {ner_model} (CPU)")
        except Exception as e:
            print(f"❌ Error loading NER model: {e}")
            self.ner_pipe = None
        
        try:
            with open(data_path, 'r') as f:
                self.kg_data = json.load(f)
            print(f"✅ Knowledge graph data loaded: {len(self.kg_data)} entities")
        except Exception as e:
            print(f"❌ Error loading knowledge graph data: {e}")
            self.kg_data = []

    def extract_entities(self, text: str) -> List[str]:
        """Extracts key entities from the text."""
        try:
            if not self.ner_pipe:
                # Fallback to simple keyword extraction
                return self._extract_keywords(text)
            
            entities = self.ner_pipe(text)
            # Filter for relevant entities
            extracted_entities = []
            for entity in entities:
                if entity['entity'].startswith('B-') or entity['entity'].startswith('I-'):
                    # Clean up entity text
                    entity_text = entity['word'].replace('##', '')
                    if entity_text not in extracted_entities:
                        extracted_entities.append(entity_text)
            
            return extracted_entities
        except Exception as e:
            print(f"Error extracting entities: {e}")
            return self._extract_keywords(text)

    def _extract_keywords(self, text: str) -> List[str]:
        """Fallback keyword extraction using simple pattern matching."""
        # Common educational keywords
        educational_keywords = [
            'photosynthesis', 'cellular respiration', 'mitochondria', 'chloroplast',
            'artificial intelligence', 'machine learning', 'neural network',
            'general relativity', 'einstein', 'turing', 'world war',
            'biology', 'chemistry', 'physics', 'mathematics', 'history',
            'computer science', 'programming', 'algorithm', 'data structure'
        ]
        
        text_lower = text.lower()
        found_keywords = []
        
        for keyword in educational_keywords:
            if keyword in text_lower:
                found_keywords.append(keyword)
        
        return found_keywords

    def query_knowledge_base(self, entities: List[str]) -> Optional[str]:
        """Queries the knowledge base for information about entities."""
        if not entities or not self.kg_data:
            return None
        
        results = []
        for item in self.kg_data:
            # Check if any entity matches the knowledge graph item
            if any(self._entity_matches(entity, item) for entity in entities):
                # Include summary and description
                result_text = f"{item.get('summary', '')} {item.get('description', '')}"
                results.append(result_text)
        
        return " ".join(results) if results else None

    def _entity_matches(self, entity: str, kg_item: Dict) -> bool:
        """Check if an entity matches a knowledge graph item."""
        entity_lower = entity.lower()
        item_entity = kg_item.get('entity', '').lower()
        aliases = [alias.lower() for alias in kg_item.get('aliases', [])]
        
        # Direct match
        if entity_lower in item_entity or item_entity in entity_lower:
            return True
        
        # Alias match
        if any(alias in entity_lower or entity_lower in alias for alias in aliases):
            return True
        
        # Partial match
        if entity_lower in item_entity.split() or any(word in entity_lower for word in item_entity.split()):
            return True
        
        return False

    def search_knowledge(self, query: str) -> List[Dict]:
        """Search the knowledge base for relevant information."""
        if not query or not self.kg_data:
            return []
        
        query_lower = query.lower()
        results = []
        
        for item in self.kg_data:
            relevance_score = 0
            
            # Check entity name
            if query_lower in item.get('entity', '').lower():
                relevance_score += 3
            
            # Check aliases
            for alias in item.get('aliases', []):
                if query_lower in alias.lower():
                    relevance_score += 2
            
            # Check summary
            if query_lower in item.get('summary', '').lower():
                relevance_score += 1
            
            # Check description
            if query_lower in item.get('description', '').lower():
                relevance_score += 1
            
            # Check properties
            for prop_value in item.get('properties', {}).values():
                if isinstance(prop_value, str) and query_lower in prop_value.lower():
                    relevance_score += 1
                elif isinstance(prop_value, list):
                    for val in prop_value:
                        if query_lower in str(val).lower():
                            relevance_score += 1
            
            if relevance_score > 0:
                results.append({
                    'item': item,
                    'relevance_score': relevance_score
                })
        
        # Sort by relevance score
        results.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return results[:5]  # Return top 5 results

    def get_related_topics(self, entities: List[str]) -> List[str]:
        """Get related topics based on entities."""
        if not entities or not self.kg_data:
            return []
        
        related_topics = set()
        
        for entity in entities:
            for item in self.kg_data:
                if self._entity_matches(entity, item):
                    # Add related entities from relationships
                    for relationship in item.get('relationships', []):
                        target_id = relationship.get('target_id')
                        if target_id:
                            # Find the related item
                            related_item = next((i for i in self.kg_data if i.get('id') == target_id), None)
                            if related_item:
                                related_topics.add(related_item.get('entity', ''))
        
        return list(related_topics)[:10]  # Limit to 10 topics

    def get_related_content(self, entities: List[str]) -> List[Dict]:
        """Get related content based on entities."""
        if not entities or not self.kg_data:
            return []
        
        related_content = []
        
        for entity in entities:
            for item in self.kg_data:
                if self._entity_matches(entity, item):
                    # Add the main item
                    related_content.append({
                        'type': 'main_topic',
                        'entity': item.get('entity'),
                        'summary': item.get('summary'),
                        'description': item.get('description')
                    })
                    
                    # Add related items
                    for relationship in item.get('relationships', []):
                        target_id = relationship.get('target_id')
                        if target_id:
                            related_item = next((i for i in self.kg_data if i.get('id') == target_id), None)
                            if related_item:
                                related_content.append({
                                    'type': 'related_topic',
                                    'entity': related_item.get('entity'),
                                    'summary': related_item.get('summary'),
                                    'relationship': relationship.get('relation_type'),
                                    'description': relationship.get('description')
                                })
        
        return related_content[:10]  # Limit to 10 items

    def get_entity_details(self, entity_name: str) -> Optional[Dict]:
        """Get detailed information about a specific entity."""
        if not entity_name or not self.kg_data:
            return None
        
        for item in self.kg_data:
            if self._entity_matches(entity_name, item):
                return item
        
        return None

    def get_knowledge_graph_stats(self) -> Dict:
        """Get statistics about the knowledge graph."""
        if not self.kg_data:
            return {"total_entities": 0}
        
        entity_types = {}
        total_relationships = 0
        
        for item in self.kg_data:
            entity_type = item.get('type', 'Unknown')
            entity_types[entity_type] = entity_types.get(entity_type, 0) + 1
            total_relationships += len(item.get('relationships', []))
        
        return {
            "total_entities": len(self.kg_data),
            "entity_types": entity_types,
            "total_relationships": total_relationships,
            "average_relationships_per_entity": total_relationships / len(self.kg_data) if self.kg_data else 0
        }