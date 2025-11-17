from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def hello():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Page</title>
    </head>
    <body>
        <h1>🎓 AI Virtual Assistant Test</h1>
        <p>If you can see this, the web server is working!</p>
        <p>Status: ✅ Server is running</p>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == '__main__':
    print("Starting minimal Flask test server...")
    print("Visit: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
