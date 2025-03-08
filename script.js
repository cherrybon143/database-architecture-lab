const API_URL = "http://127.0.0.1:5000";

async function loadProducts() {
    let response = await fetch(`${API_URL}/products`);
    let products = await response.json();

    let productTable = document.getElementById("product-list");
    productTable.innerHTML = ""; 

    products.forEach(product => {
        let row = `<tr>
            <td>${product.id}</td>
            <td>${product.name}</td>
            <td>$${product.price}</td>
            <td>${product.stock}</td>
            <td><button onclick="deleteProduct(${product.id})">Delete</button></td>
        </tr>`;
        productTable.innerHTML += row;
    });
}

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

window.onload = loadProducts;
