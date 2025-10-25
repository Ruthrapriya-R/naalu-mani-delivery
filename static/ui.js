document.addEventListener('DOMContentLoaded', function() {
  console.log("✅ ui.js loaded");

  const cartControls = document.querySelectorAll('.cart-controls');

  cartControls.forEach(control => {
    const addBtn = control.querySelector('.add-btn');
    const qtyBox = control.querySelector('.quantity-box');
    const decrease = control.querySelector('.decrease');
    const increase = control.querySelector('.increase');
    const input = control.querySelector('input[name="quantity"]');

    if (!addBtn) return;

    addBtn.addEventListener('click', () => {
      console.log("🧩 Add button detected for item:", control.dataset.id);
      const quantity = parseInt(input.value);
      const itemId = control.dataset.id;

      fetch(`/add_to_cart/${itemId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ quantity: quantity })
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          showToast(`${data.name} added to cart 🛒`);
          updateCartCount();

          // 🛒 Animate
          flyToCart(control.closest('.item-card').querySelector('img'));

          const cartIcon = document.querySelector('.fa-shopping-cart');
          if (cartIcon) {
            cartIcon.classList.add('cart-glow');
            setTimeout(() => cartIcon.classList.remove('cart-glow'), 500);
          }

          addBtn.style.display = 'none';
          qtyBox.style.display = 'flex';
        } else {
          showToast("Error adding item ❌");
        }
      })
      .catch(err => {
        console.error('Add to cart error:', err);
        showToast("Server error ❌");
      });
    });

    if (increase) {
      increase.addEventListener('click', () => {
        input.value = parseInt(input.value) + 1;
      });
    }

    if (decrease) {
      decrease.addEventListener('click', () => {
        if (parseInt(input.value) > 1) {
          input.value = parseInt(input.value) - 1;
        }
      });
    }
  });

  function showToast(message) {
    const toast = document.getElementById('addToast');
    if (!toast) return;
    toast.innerText = message;
    toast.style.display = 'block';
    setTimeout(() => { toast.style.display = 'none'; }, 1500);
  }

  function updateCartCount() {
    fetch('/cart_count')
      .then(res => res.json())
      .then(data => {
        const countElement = document.getElementById('cart-count');
        if (countElement) {
          countElement.textContent = data.count;
          countElement.classList.add('bounce');
          setTimeout(() => countElement.classList.remove('bounce'), 400);
        }
      })
      .catch(err => console.error('Cart count update error:', err));
  }

  updateCartCount();
});

// 🛒 Flying Image Animation
function flyToCart(imageElement) {
  const cartIcon = document.querySelector('.fa-shopping-cart');
  if (!imageElement || !cartIcon) return;

  const imgClone = imageElement.cloneNode(true);
  const imgRect = imageElement.getBoundingClientRect();
  const cartRect = cartIcon.getBoundingClientRect();

  imgClone.classList.add('flying-item');
  document.body.appendChild(imgClone);

  imgClone.style.left = `${imgRect.left}px`;
  imgClone.style.top = `${imgRect.top}px`;
  imgClone.style.transform = 'scale(1)';

  setTimeout(() => {
    imgClone.style.left = `${cartRect.left}px`;
    imgClone.style.top = `${cartRect.top}px`;
    imgClone.style.transform = 'scale(0.2)';
    imgClone.style.opacity = '0';
  }, 50);

  setTimeout(() => {
    cartIcon.classList.add('cart-shake');
    setTimeout(() => cartIcon.classList.remove('cart-shake'), 400);
  }, 700);

  setTimeout(() => {
    imgClone.remove();
  }, 800);
}

// 📩 Fake contact form handler
function sendMessage(event) {
  event.preventDefault();
  const name = document.getElementById("name").value.trim();

  if (name) {
    alert(`Thank you, ${name}! Your message has been sent successfully 💜`);
    document.getElementById("contactForm").reset();
  } else {
    alert("Please fill in all the fields before submitting.");
  }
  return false;
}
