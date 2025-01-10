let users = JSON.parse(localStorage.getItem('users')) || [];
let cart = [];

// Mostrar el formulario de registro
function showRegister() {
    document.getElementById('login-container').classList.add('hidden');
    document.getElementById('register-container').classList.remove('hidden');
}

// Volver al login desde el registro
function backToLogin() {
    document.getElementById('register-container').classList.add('hidden');
    document.getElementById('login-container').classList.remove('hidden');
}

// Registrar usuario
function registerUser() {
    const username = document.getElementById('register-username').value.trim();
    const password = document.getElementById('register-password').value.trim();

    if (!username || !password) {
        alert('Por favor, complete todos los campos.');
        return;
    }

    if (users.some(user => user.username === username)) {
        alert('El usuario ya existe.');
        return;
    }

    users.push({ username, password });
    localStorage.setItem('users', JSON.stringify(users));
    alert('Usuario registrado correctamente.');
    backToLogin();
}

// Iniciar sesión
function login() {
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value.trim();

    if (!username || !password) {
        alert('Por favor, complete todos los campos.');
        return;
    }

    const user = users.find(user => user.username === username && user.password === password);
    if (user) {
        alert('Inicio de sesión exitoso.');
        localStorage.setItem('loggedUser', username);
        loadUserInterface();
    } else {
        alert('Usuario o contraseña incorrectos.');
    }
}

// Cargar la interfaz según el usuario autenticado
function loadUserInterface() {
    const loggedUser = localStorage.getItem('loggedUser');

    if (loggedUser) {
        document.getElementById('login-container').classList.add('hidden');
        document.getElementById('register-container').classList.add('hidden');
        document.getElementById('description-container').classList.remove('hidden');
    } else {
        document.getElementById('login-container').classList.remove('hidden');
        document.getElementById('description-container').classList.add('hidden');
        document.getElementById('menu-container').classList.add('hidden');
        document.getElementById('cart-container').classList.add('hidden');
    }
}

// Cerrar sesión
function logout() {
    localStorage.removeItem('loggedUser');
    alert('Sesión cerrada.');
    loadUserInterface();
}

// Mostrar menú de comida
function showMenu() {
    document.getElementById('description-container').classList.add('hidden');
    document.getElementById('menu-container').classList.remove('hidden');
}

// Volver a la pantalla de bienvenida
function backToDescription() {
    document.getElementById('menu-container').classList.add('hidden');
    document.getElementById('description-container').classList.remove('hidden');
}

// Agregar productos al carrito
function addToCart(item, price, quantityId) {
    const quantity = parseInt(document.getElementById(quantityId).value);

    if (isNaN(quantity) || quantity <= 0) {
        alert('La cantidad debe ser mayor a 0.');
        return;
    }

    cart.push({ item, quantity, total: quantity * price });
    alert(`${quantity} ${item}(s) agregado(s) al carrito.`);
}

// Ver carrito
function viewCart() {
    const cartItems = document.getElementById('cart-items');
    const cartTotal = document.getElementById('cart-total');

    cartItems.innerHTML = '';
    let total = 0;

    if (cart.length === 0) {
        cartItems.innerHTML = '<li>El carrito está vacío</li>';
        cartTotal.innerText = 'Total: $0';
    } else {
        cart.forEach(({ item, quantity, total: itemTotal }, index) => {
            total += itemTotal;
            const li = document.createElement('li');
            li.innerHTML = `${quantity} x ${item} - $${itemTotal} 
                <button onclick="removeFromCart(${index})">❌</button>`;
            cartItems.appendChild(li);
        });
        cartTotal.innerText = `Total: $${total}`;
    }

    document.getElementById('menu-container').classList.add('hidden');
    document.getElementById('cart-container').classList.remove('hidden');
}

// Eliminar producto del carrito
function removeFromCart(index) {
    cart.splice(index, 1);
    viewCart();
}

// Volver al menú desde el carrito
function backToMenu() {
    document.getElementById('cart-container').classList.add('hidden');
    document.getElementById('menu-container').classList.remove('hidden');
}

// Pagar productos del carrito
function checkout() {
    if (cart.length === 0) {
        alert('El carrito está vacío.');
        return;
    }

    alert('Compra realizada con éxito. ¡Gracias por tu pedido!');
    cart = [];
    viewCart();
    backToMenu();
}

// Cargar la interfaz al iniciar la página
window.onload = function () {
    loadUserInterface();
};
