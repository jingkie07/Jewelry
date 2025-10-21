from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'elegant_diy_jewelry_secret'


# ---- HOME PAGE ----
@app.route('/')
def home():
    featured_products = [
        {'name': 'Pearl Elegance Bracelet', 'price': 39.99, 'image': 'bracelet.jpg', 'desc': 'Classic pearls handcrafted with care.'},
        {'name': 'Crystal Bloom Necklace', 'price': 55.00, 'image': 'necklace.jpg', 'desc': 'Sparkling crystals shaped like blossoms.'},
        {'name': 'Golden Charm Ring', 'price': 29.99, 'image': 'ring.jpg', 'desc': 'A minimal, chic ring for any outfit.'},
    ]
    return render_template('home.html', title='DIY Jewelry | Home', featured=featured_products)


# ---- ABOUT PAGE ----
@app.route('/about')
def about():
    return render_template('about.html', title='About Us')


# ---- SHOP PAGE ----
@app.route('/shop')
def shop():
    products = [
        {'name': 'Amethyst Dream Earrings', 'price': 24.99, 'desc': 'Elegant violet tones for a subtle sparkle.'},
        {'name': 'Silver Petal Bracelet', 'price': 34.50, 'desc': 'Delicate silver petals interlinked gracefully.'},
        {'name': 'Ocean Blue Necklace', 'price': 48.00, 'desc': 'Handcrafted with sea-inspired gemstones.'},
        {'name': 'Rose Quartz Ring', 'price': 28.00, 'desc': 'Gentle pink gemstone symbolizing love.'},
        {'name': 'Golden Sunset Anklet', 'price': 22.50, 'desc': 'A light, summery accessory with gold beads.'},
    ]
    return render_template('shop.html', title='Shop DIY Jewelry', products=products)


# ---- CONTACT PAGE ----
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        if name and email and message:
            flash('Thank you for contacting us! We’ll reply soon.', 'success')
            return redirect(url_for('contact'))
        else:
            flash('Please fill in all fields before submitting.', 'danger')

    return render_template('contact.html', title='Contact Us')


if __name__ == '__main__':
    app.run(debug=True)
