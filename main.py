from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure key in production

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('aboutus.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        # You can add email sending or DB storage here
        print(f"Contact form submitted: {name}, {email}, {message}")
        flash("Thank you for contacting us! We'll get back to you soon.", "success")
        return redirect(url_for('contact'))
    return render_template('contactus.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        product = request.form.get('product')
        quantity = request.form.get('quantity')
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        print(f"Order received: {product}, {quantity}, {name}, {email}, {phone}")
        flash("Your order has been submitted successfully!", "success")
        return redirect(url_for('order'))
    return render_template('order.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)
