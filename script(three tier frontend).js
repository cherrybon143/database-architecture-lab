const API_URL = "http://127.0.0.1:5000";

// Load products when the page opens
async function loadProducts() {
    let response = await fetch(`${API_URL}/products`);
    let products = await response.json();

    let productList = document.getElementById("product-list");
    productList.innerHTML = "";  

    products.forEach(product => {
        let item = document.createElement("li");
        item.innerHTML = `${product.name} - $${product.price} (${product.stock} in stock) 
            <button onclick="deleteProduct(${product.id})">Delete</button>`;
        productList.appendChild(item);
    });
}

// Add a new product
async function addProduct() {
    let name = document.getElementById("name").value;
    let price = document.getElementById("price").value;
    let stock = document.getElementById("stock").value;

    let response = await fetch(`${API_URL}/add_product`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, price, stock })
    });

    if (response.ok) {
        alert("Product added successfully!");
        loadProducts();
    } else {
        alert("Failed to add product.");
    }
}

// Delete a product
async function deleteProduct(id) {
    let confirmDelete = confirm("Are you sure you want to delete this product?");
    if (!confirmDelete) return;

    let response = await fetch(`${API_URL}/delete_product/${id}`, {
        method: "DELETE"
    });

    if (response.ok) {
        alert("Product deleted successfully!");
        loadProducts();
    } else {
        let errorData = await response.json();
        alert("Failed to delete product: " + errorData.error);
    }
}

// Load products on page load
window.onload = loadProducts;
