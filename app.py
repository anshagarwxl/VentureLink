from flask import Flask, render_template, request, redirect, session, flash
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', "venturelink_secret_key_2024")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['role'] = request.form.get('role')
        return redirect('/dashboard')
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>VentureLink - Vercel Demo</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gradient-to-br from-blue-500 to-purple-600 min-h-screen flex items-center justify-center">
    <div class="max-w-md w-full bg-white rounded-2xl shadow-2xl p-8 mx-4">
        <div class="text-center mb-8">
            <div class="w-20 h-20 bg-gradient-to-r from-blue-500 to-purple-600 rounded-2xl mx-auto flex items-center justify-center mb-4">
                <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                </svg>
            </div>
            <h1 class="text-3xl font-bold text-gray-900 mb-2">VentureLink</h1>
            <p class="text-gray-600">Production Ready on Vercel! 🎉</p>
        </div>
        
        <form method="POST" class="space-y-4">
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Select Role</label>
                <select name="role" class="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                    <option value="">Choose...</option>
                    <option value="startup">🚀 Startup</option>
                    <option value="investor">💰 Investor</option>
                </select>
            </div>
            <button type="submit" class="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white font-semibold py-3 px-4 rounded-xl hover:from-blue-600 hover:to-purple-700 transition-all duration-200 shadow-lg">
                Enter Dashboard
            </button>
        </form>
        
        <div class="mt-8 pt-6 border-t border-gray-200 text-center">
            <p class="text-sm text-gray-500">
                Local: <a href="http://localhost:5050" class="text-blue-600 hover:underline">localhost:5050</a><br>
                GitHub: <a href="https://github.com/anshagarwxl/VentureLink-.git" class="text-blue-600 hover:underline" target="_blank">Repo</a>
            </p>
        </div>
    </div>
</body>
</html>
    '''

@app.route('/dashboard')
def dashboard():
    role = session.get('role', 'guest')
    return f'''
<!DOCTYPE html>
<html>
<head>
    <title>Dashboard - {role.title()}</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 min-h-screen p-8">
    <div class="max-w-4xl mx-auto">
        <div class="bg-white rounded-2xl shadow-xl p-8 mb-8">
            <h1 class="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-4">
                Welcome {role.title()}! 🎉
            </h1>
            <p class="text-xl text-gray-600 mb-8">Vercel Deployment SUCCESSFUL!</p>
            
            <div class="grid md:grid-cols-2 gap-6">
                <div class="bg-gradient-to-br from-green-400 to-blue-500 text-white p-8 rounded-xl">
                    <div class="text-4xl mb-2">28</div>
                    <div>Total Startups</div>
                </div>
                <div class="bg-gradient-to-br from-purple-400 to-pink-500 text-white p-8 rounded-xl">
                    <div class="text-4xl mb-2">12</div>
                    <div>Total Investors</div>
                </div>
            </div>
            
            <div class="mt-8 p-6 bg-blue-50 border border-blue-200 rounded-xl">
                <h3 class="text-lg font-semibold text-blue-900 mb-2">✅ Features Working:</h3>
                <ul class="text-blue-800 space-y-1">
                    <li>✓ Serverless Functions</li>
                    <li>✓ Vercel Routing</li>
                    <li>✓ Session Management</li>
                    <li>✓ Responsive Design</li>
                    <li>✓ Tailwind CSS</li>
                </ul>
            </div>
        </div>
        
        <div class="text-center">
            <a href="/" class="inline-flex items-center px-8 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-semibold rounded-xl hover:from-blue-600 hover:to-purple-700 transition-all duration-200 shadow-lg">
                ← Back to Login
            </a>
        </div>
    </div>
</body>
</html>
    '''

@app.errorhandler(404)
def not_found(e):
    return "Page not found. Go to <a href='/'>Home</a>", 404

@app.errorhandler(500)
def internal_error(e):
    return "Server error. Local works fine! Check Vercel logs.", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

