document.addEventListener('DOMContentLoaded', () => {
    const productList = document.getElementById('product-list');
    const saleProduct = document.getElementById('sale-product');
    const saleQuantity = document.getElementById('sale-quantity');
    const recordSaleButton = document.getElementById('record-sale-button');
    const inventoryList = document.getElementById('inventory-list');
    const newProductName = document.getElementById('new-product-name');
    const newProductPrice = document.getElementById('new-product-price');
    const addProductButton = document.getElementById('add-product-button');
    const newUserName = document.getElementById('new-user-name');
    const newUserPassword = document.getElementById('new-user-password');
    const newUserRole = document.getElementById('new-user-role');
    const addUserButton = document.getElementById('add-user-button');

    // Fetch products and populate the product list and sale product dropdown
    fetch('/products')
        .then(response => response.json())
        .then(products => {
            products.forEach(product => {
                const li = document.createElement('li');
                li.textContent = `${product.name} - $${product.price}`;
                productList.appendChild(li);

                const option = document.createElement('option');
                option.value = product.id;
                option.textContent = product.name;
                saleProduct.appendChild(option);
            });
        });

    // Fetch inventory and populate the inventory list
    fetch('/inventory')
        .then(response => response.json())
        .then(inventory => {
            inventory.forEach(item => {
                const li = document.createElement('li');
                li.textContent = `Product ID: ${item.product_id}, Quantity: ${item.quantity}`;
                inventoryList.appendChild(li);
            });
        });

    // Record sale
    recordSaleButton.addEventListener('click', () => {
        fetch('/sales', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                product_id: parseInt(saleProduct.value),
                quantity: parseInt(saleQuantity.value)
            })
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
        });
    });

    // Add product
    addProductButton.addEventListener('click', () => {
        fetch('/add_product', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: newProductName.value,
                price: parseFloat(newProductPrice.value)
            })
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
        });
    });

    // Add user
    addUserButton.addEventListener('click', () => {
      fetch('/add_user', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          username: newUserName.value,
          password: newUserPassword.value, //Hash password in production
          role: newUserRole.value
        })
      })
      .then(response => response.json())
      .then(data => {
        alert(data.message);
      });
    });
});
