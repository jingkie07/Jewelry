from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'elegant_diy_jewelry_secret'

# Fake database (temporary)
users = {}

# ---- HOME PAGE ----
@app.route('/')
def home():
    featured_products = [
        {'name': 'Pearl Elegance Bracelet', 'price': 39.99, 'image': 'bracelet.jpg', 'desc': 'Classic pearls handcrafted with care.'},
        {'name': 'Crystal Bloom Necklace', 'price': 55.00, 'image': 'necklace.jpg', 'desc': 'Sparkling crystals shaped like blossoms.'},
        {'name': 'Golden Charm Ring', 'price': 29.99, 'image': 'ring.jpg', 'desc': 'A minimal, chic ring for any outfit.'},
    ]
    user = session.get('user')
    return render_template('home.html', title='DIY Jewelry | Home', featured=featured_products, user=user)


# ---- ABOUT PAGE ----
@app.route('/about')
def about():
    user = session.get('user')
    return render_template('about.html', title='About Us', user=user)


# ---- SHOP PAGE ----
@app.route('/shop')
def shop():
    user = session.get('user')
    products = [
        {'name': 'Amethyst Dream Earrings', 'price': 24.99, 'desc': 'Elegant violet tones for a subtle sparkle.'},
        {'name': 'Silver Petal Bracelet', 'price': 34.50, 'desc': 'Delicate silver petals interlinked gracefully.'},
        {'name': 'Ocean Blue Necklace', 'price': 48.00, 'desc': 'Handcrafted with sea-inspired gemstones.'},
        {'name': 'Rose Quartz Ring', 'price': 28.00, 'desc': 'Gentle pink gemstone symbolizing love.'},
        {'name': 'Golden Sunset Anklet', 'price': 22.50, 'desc': 'A light, summery accessory with gold beads.'},
    ]
    return render_template('shop.html', title='Shop DIY Jewelry', products=products, user=user)


# ---- CONTACT PAGE ----
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    user = session.get('user')
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        if name and email and message:
            flash('Thank you for contacting us! We’ll reply soon.', 'success')
            return redirect(url_for('contact'))
        else:
            flash('Please fill in all fields before submitting.', 'danger')

    return render_template('contact.html', title='Contact Us', user=user)


# ---- SIGN UP PAGE ----
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if email in users:
            flash('Email already registered.')
        else:
            users[email] = {'username': username, 'password': password}
            flash('Signup successful! You can now log in.')
            return redirect(url_for('login'))
    return render_template('signup.html', user=session.get('user'))


# ---- LOGIN PAGE ----
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = users.get(email)
        if user and user['password'] == password:
            session['user'] = user['username']
            flash(f'Welcome back, {user["username"]}!')
            return redirect(url_for('shop'))  # Redirect to shop after login
        else:
            flash('Invalid email or password.')
    return render_template('login.html', user=session.get('user'))


# ---- LOGOUT ----
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
