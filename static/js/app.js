// ByteBite Bistro - Client Application Logic

document.addEventListener('DOMContentLoaded', () => {
    // State
    let menuItems = [];
    let currentCategory = 'All';
    let currentSearch = '';
    let sessionId = localStorage.getItem('bytebite_session_id') || null;

    // DOM Elements
    const menuGrid = document.getElementById('menuGrid');
    const categoryTabsContainer = document.getElementById('categoryTabsContainer');
    const menuSearchInput = document.getElementById('menuSearchInput');
    const cartCountBadge = document.getElementById('cartCountBadge');
    
    // Chat Elements
    const chatForm = document.getElementById('chatForm');
    const chatInput = document.getElementById('chatInput');
    const chatMessages = document.getElementById('chatMessages');
    const typingIndicator = document.getElementById('typingIndicator');
    const clearChatBtn = document.getElementById('clearChatBtn');
    
    // Cart Drawer Elements
    const cartDrawer = document.getElementById('cartDrawer');
    const cartOverlay = document.getElementById('cartOverlay');
    const openCartBtn = document.getElementById('openCartBtn');
    const closeCartBtn = document.getElementById('closeCartBtn');
    const cartItemsList = document.getElementById('cartItemsList');
    const billSubtotal = document.getElementById('billSubtotal');
    const billTax = document.getElementById('billTax');
    const billTotal = document.getElementById('billTotal');
    const clearCartBtn = document.getElementById('clearCartBtn');
    const checkoutBtn = document.getElementById('checkoutBtn');
    const askAiToOrderBtn = document.getElementById('askAiToOrderBtn');
    
    // Modal Elements
    const orderModal = document.getElementById('orderModal');
    const closeModalBtn = document.getElementById('closeModalBtn');
    const trackOrderNavBtn = document.getElementById('trackOrderNavBtn');
    const trackOrderIdInput = document.getElementById('trackOrderIdInput');
    const searchOrderBtn = document.getElementById('searchOrderBtn');
    const orderResult = document.getElementById('orderResult');

    // Emoji Mapping for categories / dishes
    const emojiMap = {
        "Burgers": "🍔",
        "Pizza": "🍕",
        "Sides": "🍟",
        "Drinks": "🥤",
        "Chicken": "🍗",
        "Salad": "🥗"
    };

    function getFoodIcon(name, category) {
        if (emojiMap[category]) return emojiMap[category];
        const lower = name.toLowerCase();
        if (lower.includes('burger')) return '🍔';
        if (lower.includes('pizza')) return '🍕';
        if (lower.includes('coke') || lower.includes('pepsi') || lower.includes('drink')) return '🥤';
        if (lower.includes('fries')) return '🍟';
        if (lower.includes('wing') || lower.includes('chicken')) return '🍗';
        return '🍽️';
    }

    // ==================== Init App ====================
    fetchMenu();
    fetchCart();

    // ==================== Menu Logic ====================
    async function fetchMenu() {
        try {
            const res = await fetch('/api/menu');
            const data = await res.json();
            menuItems = data.items || [];
            renderCategories(data.categories || []);
            renderMenu();
        } catch (err) {
            console.error("Failed to load menu:", err);
            menuGrid.innerHTML = `<div class="error-msg">Failed to load menu. Please check your connection.</div>`;
        }
    }

    function renderCategories(categories) {
        categoryTabsContainer.innerHTML = `<button class="cat-tab active" data-category="All">🔥 All Items</button>`;
        categories.forEach(cat => {
            const icon = emojiMap[cat] || '🍽️';
            const btn = document.createElement('button');
            btn.className = 'cat-tab';
            btn.dataset.category = cat;
            btn.textContent = `${icon} ${cat}`;
            btn.addEventListener('click', () => {
                document.querySelectorAll('.cat-tab').forEach(t => t.classList.remove('active'));
                btn.classList.add('active');
                currentCategory = cat;
                renderMenu();
            });
            categoryTabsContainer.appendChild(btn);
        });

        // Event listener for "All"
        categoryTabsContainer.querySelector('[data-category="All"]').addEventListener('click', (e) => {
            document.querySelectorAll('.cat-tab').forEach(t => t.classList.remove('active'));
            e.target.classList.add('active');
            currentCategory = 'All';
            renderMenu();
        });
    }

    function renderMenu() {
        const filtered = menuItems.filter(item => {
            const matchCat = (currentCategory === 'All' || item.category === currentCategory);
            const matchSearch = item.name.toLowerCase().includes(currentSearch.toLowerCase()) || 
                                item.description.toLowerCase().includes(currentSearch.toLowerCase());
            return matchCat && matchSearch;
        });

        if (filtered.length === 0) {
            menuGrid.innerHTML = `
                <div style="grid-column: 1/-1; text-align: center; padding: 2rem; color: var(--text-muted);">
                    <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🔍</div>
                    <p>No dishes found matching your search.</p>
                </div>
            `;
            return;
        }

        menuGrid.innerHTML = filtered.map(item => `
            <div class="menu-card" data-id="${item.id}">
                <div>
                    <div class="card-top">
                        <div class="card-food-icon">${getFoodIcon(item.name, item.category)}</div>
                        <span class="card-category-tag">${item.category}</span>
                    </div>
                    <h3 class="card-title">${item.name}</h3>
                    <p class="card-desc">${item.description}</p>
                </div>
                <div class="card-footer">
                    <span class="card-price">$${item.price.toFixed(2)}</span>
                    <button class="btn-card-add" onclick="handleAddToCart(${item.id})">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
                        <span>Add</span>
                    </button>
                </div>
            </div>
        `).join('');
    }

    menuSearchInput.addEventListener('input', (e) => {
        currentSearch = e.target.value;
        renderMenu();
    });

    // ==================== Cart Logic ====================
    window.handleAddToCart = async function(itemId) {
        try {
            const res = await fetch('/api/cart/add', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ item_id: itemId, quantity: 1 })
            });
            const data = await res.json();
            updateCartUI(data.cart);
            showToast('Added to cart! 🛒', 'success');
        } catch (err) {
            console.error("Error adding to cart:", err);
        }
    };

    async function fetchCart() {
        try {
            const res = await fetch('/api/cart');
            const cartData = await res.json();
            updateCartUI(cartData);
        } catch (err) {
            console.error("Failed to fetch cart:", err);
        }
    }

    function updateCartUI(cart) {
        if (!cart) return;
        cartCountBadge.textContent = cart.count || 0;

        if (!cart.items || cart.items.length === 0) {
            cartItemsList.innerHTML = `
                <div class="cart-empty-state">
                    <div class="empty-icon">🛒</div>
                    <h4>Your cart is empty</h4>
                    <p>Ask our AI agent or click dishes on the menu to start your order!</p>
                </div>
            `;
            billSubtotal.textContent = '$0.00';
            billTax.textContent = '$0.00';
            billTotal.textContent = '$0.00';
            return;
        }

        cartItemsList.innerHTML = cart.items.map(item => `
            <div class="cart-item-card">
                <div class="cart-item-info">
                    <div class="cart-item-title">${item.name}</div>
                    <div class="cart-item-price">$${item.price.toFixed(2)} each</div>
                </div>
                <div class="cart-item-controls">
                    <button class="qty-btn" onclick="handleUpdateCartQty(${item.id}, -1)">−</button>
                    <span class="qty-val">${item.quantity}</span>
                    <button class="qty-btn" onclick="handleUpdateCartQty(${item.id}, 1)">+</button>
                </div>
            </div>
        `).join('');

        billSubtotal.textContent = `$${cart.subtotal.toFixed(2)}`;
        billTax.textContent = `$${cart.tax.toFixed(2)}`;
        billTotal.textContent = `$${cart.total.toFixed(2)}`;
    }

    window.handleUpdateCartQty = async function(itemId, delta) {
        try {
            const res = await fetch('/api/cart/update', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ item_id: itemId, delta: delta })
            });
            const cart = await res.json();
            updateCartUI(cart);
        } catch (err) {
            console.error("Failed to update item quantity:", err);
        }
    };

    clearCartBtn.addEventListener('click', async () => {
        if (!confirm('Clear all items from your cart?')) return;
        try {
            const res = await fetch('/api/cart/clear', { method: 'POST' });
            const cart = await res.json();
            updateCartUI(cart);
            showToast('Cart cleared', 'info');
        } catch (err) {
            console.error("Failed to clear cart:", err);
        }
    });

    checkoutBtn.addEventListener('click', async () => {
        try {
            const res = await fetch('/api/orders/place', { method: 'POST' });
            const data = await res.json();
            if (data.message.includes('successfully')) {
                // Extract order ID
                const match = data.message.match(/Order ID: (\d+)/);
                const orderId = match ? match[1] : 1;
                updateCartUI(data.cart);
                closeCart();
                openTrackingModal(orderId);
                showToast('Order placed successfully! 🎉', 'success');
            } else {
                showToast(data.message, 'info');
            }
        } catch (err) {
            console.error("Checkout failed:", err);
        }
    });

    askAiToOrderBtn.addEventListener('click', () => {
        closeCart();
        sendChatMessage("Please place my current cart order now.");
    });

    // Drawer toggles
    openCartBtn.addEventListener('click', () => {
        cartDrawer.classList.add('open');
        cartOverlay.classList.add('open');
    });
    const closeCart = () => {
        cartDrawer.classList.remove('open');
        cartOverlay.classList.remove('open');
    };
    closeCartBtn.addEventListener('click', closeCart);
    cartOverlay.addEventListener('click', closeCart);

    // ==================== AI Chat Logic ====================
    chatForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const text = chatInput.value.trim();
        if (!text) return;
        sendChatMessage(text);
        chatInput.value = '';
    });

    // Quick prompt buttons
    document.querySelectorAll('.prompt-chip').forEach(chip => {
        chip.addEventListener('click', () => {
            const prompt = chip.dataset.prompt;
            sendChatMessage(prompt);
        });
    });

    async function sendChatMessage(userText) {
        // Append user message
        appendMessage('user', userText);
        typingIndicator.style.display = 'flex';
        chatMessages.scrollTop = chatMessages.scrollHeight;

        try {
            const res = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: userText, session_id: sessionId })
            });
            const data = await res.json();

            if (data.session_id) {
                sessionId = data.session_id;
                localStorage.setItem('bytebite_session_id', sessionId);
            }

            // Append assistant reply
            appendMessage('assistant', data.reply);
            
            // Sync cart state if changed
            if (data.cart) {
                updateCartUI(data.cart);
            }
        } catch (err) {
            console.error("Chat error:", err);
            appendMessage('assistant', "Sorry, I had trouble processing that. Please check your connection and Gemini API Key.");
        } finally {
            typingIndicator.style.display = 'none';
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }

    function appendMessage(role, text) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${role}-message`;

        const avatar = role === 'user' ? '👤' : '🤖';
        const formattedText = formatMarkdown(text);

        msgDiv.innerHTML = `
            <div class="msg-avatar">${avatar}</div>
            <div class="msg-bubble">${formattedText}</div>
        `;
        chatMessages.appendChild(msgDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function formatMarkdown(text) {
        if (!text) return '';
        // Escape HTML
        let esc = text
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');

        // Bold
        esc = esc.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        // Bullet points
        esc = esc.replace(/^\s*[\-\*]\s+(.*)$/gm, '<li>$1</li>');
        esc = esc.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');
        // Newlines
        esc = esc.replace(/\n\n/g, '<br><br>');
        esc = esc.replace(/\n/g, '<br>');
        return esc;
    }

    clearChatBtn.addEventListener('click', () => {
        if (!confirm('Clear conversation history?')) return;
        localStorage.removeItem('bytebite_session_id');
        sessionId = null;
        chatMessages.innerHTML = `
            <div class="message assistant-message">
                <div class="msg-avatar">🤖</div>
                <div class="msg-bubble">
                    <p>Conversation reset! What can I get for you today? 🍔🍕</p>
                </div>
            </div>
        `;
    });

    // ==================== Order Tracker Modal Logic ====================
    trackOrderNavBtn.addEventListener('click', () => {
        orderModal.classList.add('open');
    });

    closeModalBtn.addEventListener('click', () => {
        orderModal.classList.remove('open');
    });

    searchOrderBtn.addEventListener('click', () => {
        const id = trackOrderIdInput.value.trim();
        if (id) openTrackingModal(id);
    });

    async function openTrackingModal(orderId) {
        orderModal.classList.add('open');
        trackOrderIdInput.value = orderId;
        
        try {
            const res = await fetch(`/api/orders/${orderId}`);
            if (!res.ok) {
                orderResult.style.display = 'block';
                orderResult.innerHTML = `
                    <div style="text-align: center; color: var(--accent-red); padding: 1rem;">
                        <p>Order #${orderId} was not found. Please verify the ID.</p>
                    </div>
                `;
                return;
            }
            const data = await res.json();
            renderOrderDetails(data.order);
        } catch (err) {
            console.error("Order lookup error:", err);
        }
    }

    function renderOrderDetails(order) {
        orderResult.style.display = 'block';
        document.getElementById('resOrderId').textContent = `Order #${order.id}`;
        document.getElementById('resOrderStatus').textContent = order.status;
        document.getElementById('resOrderTotal').textContent = `$${order.total.toFixed(2)}`;
        document.getElementById('resOrderTime').textContent = `Placed at: ${order.created_at || 'Just now'}`;

        // Render receipt items
        const receiptList = document.getElementById('receiptItemsList');
        if (Array.isArray(order.items)) {
            receiptList.innerHTML = order.items.map(i => `
                <div class="receipt-item-row">
                    <span>${i.quantity}x ${i.name}</span>
                    <span>$${(i.price * i.quantity).toFixed(2)}</span>
                </div>
            `).join('');
        }
    }

    // ==================== Toast System ====================
    function showToast(message, type = 'info') {
        const container = document.getElementById('toastContainer');
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `<span>${message}</span>`;
        container.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(100%)';
            toast.style.transition = 'all 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }
});
