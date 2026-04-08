from flask import Flask, request, render_template, flash, redirect, url_for
from flask_mail import Mail, Message
import os

app = Flask(__name__)
app.secret_key = 'zigis_plug_secret'

# Email Config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = 'maryannugwu222@gmail.com'
# REMOVE SPACES from the password string
app.config['MAIL_PASSWORD'] = 'xzlkjhgfdsapoiuy' 
app.config['MAIL_DEFAULT_SENDER'] = 'maryannugwu222@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')


mail = Mail(app)

@app.route('/')
def home():
    return render_template('home.html')

# FIX: Added 'GET' to methods so the page doesn't error out if visited directly
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message_body = request.form.get('message')

        # Basic validation to ensure data exists
        if not name or not email or not message_body:
            flash('error')
            return redirect(url_for('home'))

        msg = Message(
            subject=f"New Portfolio Message: {subject}",
            recipients=['maryannugwu222@gmail.com'],
            body=f"From: {name} ({email})\n\n{message_body}"
        )

        try:
            mail.send(msg)
            flash('success')
        except Exception as e:
            # This will print the specific reason (e.g., Auth failure) in your logs
            print(f"CRITICAL MAIL ERROR: {e}")
            flash('error')
            
        return redirect(url_for('home'))
    
    # If someone visits /contact via GET, just send them home or to a contact page
    return redirect(url_for('home'))

if __name__ == '__main__':
    # Use environment port for deployment services like Render/Heroku
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
    
