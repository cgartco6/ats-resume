<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sovereign Career Engine - Premium Workspace</title>
    <!-- Tailwind CSS for high-fidelity styling across mobile and desktop devices -->
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    <style>
        .custom-dashed { border-style: dashed; }
        .transition-all-300 { transition: all 0.3s ease; }
    </style>
</head>
<body class="bg-slate-50 font-sans text-slate-800 antialiased min-h-screen">

    <!-- Top Navigation Header -->
    <header class="bg-white border-b border-slate-200 sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <div class="flex items-center gap-3">
                <div class="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center text-white font-bold text-lg">S</div>
                <span class="font-bold text-xl tracking-tight text-slate-900">Sovereign Career Engine</span>
            </div>
            <div class="flex items-center gap-6">
                <button onclick="switchView('dashboard')" class="text-sm font-semibold text-slate-600 hover:text-blue-600 cursor-pointer transition-all-300">Workspace</button>
                <button onclick="switchView('interview')" class="text-sm font-semibold text-slate-600 hover:text-blue-600 cursor-pointer transition-all-300">AI Simulator</button>
                <div class="relative cursor-pointer" onclick="toggleCartModal()">
                    <span class="text-xl">🛒</span>
                    <span id="cart-count" class="absolute -top-2 -right-2 bg-blue-600 text-white text-xs w-5 h-5 rounded-full flex items-center justify-center font-bold">0</span>
                </div>
            </div>
        </div>
    </header>

    <!-- Main Workspace Container -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        <!-- VIEW 1: CENTRAL WORKSPACE (UPLOAD & ADD TO CART) -->
        <section id="view-dashboard" class="block transition-all-300">
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                
                <!-- Left 2 Columns: File Intake & Packages -->
                <div class="lg:col-span-2 space-y-8">
                    <!-- Clean Drag-and-Drop Area -->
                    <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-xs">
                        <h2 class="text-lg font-bold text-slate-900 mb-4">1. Upload Resume Portfolio</h2>
                        <div id="drop-zone" class="custom-dashed border-2 border-slate-300 rounded-xl p-8 flex flex-col items-center justify-center bg-slate-50 hover:bg-slate-100 transition-all-300 cursor-pointer group">
                            <input type="file" id="file-input" class="hidden" accept=".pdf,.docx,.txt" onchange="handleFileSelect(event)">
                            <div class="text-4xl mb-3 group-hover:scale-110 transition-all-300">📄</div>
                            <p class="text-sm font-medium text-slate-700 text-center">Drag and drop your raw CV here, or <span class="text-blue-600 underline">browse local files</span></p>
                            <p class="text-xs text-slate-400 mt-2">Accepts PDF, DOCX, or Plain Text strings up to 10MB</p>
                            <div id="file-meta" class="mt-4 text-sm font-semibold text-emerald-600 hidden"></div>
                        </div>
                    </div>

                    <!-- Available Premium Matrix Packages -->
                    <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-xs">
                        <h2 class="text-lg font-bold text-slate-900 mb-4">2. Select Optimization Modules</h2>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <!-- Card 1 -->
                            <div class="border border-slate-200 rounded-xl p-5 hover:border-blue-500 transition-all-300 flex flex-col justify-between">
                                <div>
                                    <span class="bg-blue-50 text-blue-700 text-xs font-bold px-2.5 py-1 rounded-sm uppercase">AI Core</span>
                                    <h3 class="font-bold text-slate-900 mt-2 text-base">Full ATS Optimization Package</h3>
                                    <p class="text-xs text-slate-500 mt-1">Calculates semantic keyword scores, matching density profiles, and strips parsing friction.</p>
                                </div>
                                <div class="mt-4 pt-4 border-t border-slate-100 flex items-center justify-between">
                                    <span class="font-extrabold text-slate-900 text-lg">R 350.00</span>
                                    <button onclick="addToCart('Full ATS Optimization Package', 350)" class="bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold px-4 py-2 rounded-lg cursor-pointer transition-all-300">Add Module</button>
                                </div>
                            </div>
                            <!-- Card 2 -->
                            <div class="border border-slate-200 rounded-xl p-5 hover:border-blue-500 transition-all-300 flex flex-col justify-between">
                                <div>
                                    <span class="bg-purple-50 text-purple-700 text-xs font-bold px-2.5 py-1 rounded-sm uppercase">Interactive</span>
                                    <h3 class="font-bold text-slate-900 mt-2 text-base">AI Interview Prep Session</h3>
                                    <p class="text-xs text-slate-500 mt-1">Unlocks interactive simulation loop including technical questions, dress codes, and calming hooks.</p>
                                </div>
                                <div class="mt-4 pt-4 border-t border-slate-100 flex items-center justify-between">
                                    <span class="font-extrabold text-slate-900 text-lg">R 450.00</span>
                                    <button onclick="addToCart('AI Interview Prep Session', 450)" class="bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold px-4 py-2 rounded-lg cursor-pointer transition-all-300">Add Module</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Right Column: Real-Time Checkout Pipeline Widget -->
                <div class="lg:col-span-1">
                    <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-xs sticky top-24">
                        <h2 class="text-lg font-bold text-slate-900 mb-4">Summary Ledger</h2>
                        <div id="cart-ledger-items" class="space-y-3 max-h-60 overflow-y-auto mb-4 pr-1">
                            <p class="text-sm text-slate-400 italic">No operational optimization modules added yet.</p>
                        </div>
                        <div class="border-t border-slate-200 pt-4 space-y-2">
                            <div class="flex justify-between text-sm text-slate-500">
                                <span>Subtotal</span>
                                <span id="ledger-subtotal">R 0.00</span>
                            </div>
                            <div class="flex justify-between text-sm text-slate-500">
                                <span>SARS VAT (15%)</span>
                                <span id="ledger-vat">R 0.00</span>
                            </div>
                            <div class="flex justify-between text-base font-bold text-slate-900 pt-2 border-t border-slate-100">
                                <span>Total Volume</span>
                                <span id="ledger-total">R 0.00</span>
                            </div>
                        </div>
                        <button onclick="triggerCheckout()" id="checkout-btn" class="w-full mt-6 bg-slate-400 text-white font-bold py-3 rounded-xl cursor-not-allowed transition-all-300 text-center text-sm" disabled>
                            Lock Configuration & Pay
                        </button>
                    </div>
                </div>

            </div>
        </section>

        <!-- VIEW 2: DYNAMIC PAYMENTS INTENT STATE LAYER -->
        <section id="view-payment" class="hidden transition-all-300 max-w-xl mx-auto">
            <div class="bg-white p-8 rounded-xl border border-slate-200 shadow-sm text-center">
                <div class="w-16 h-16 bg-blue-50 text-blue-600 rounded-full flex items-center justify-center text-2xl mx-auto mb-4 animate-pulse">💳</div>
                <h2 class="text-xl font-bold text-slate-900">Secure Commercial Checkout Gateway</h2>
                <p class="text-sm text-slate-500 mt-2">Processing localized regional security keys via anti-tamper factory layers.</p>
                
                <div class="my-6 p-4 bg-slate-50 rounded-xl text-left border border-slate-100">
                    <div class="flex justify-between font-bold text-slate-700 text-sm">
                        <span>Transaction Reference</span>
                        <span class="font-mono text-blue-600">TX-2026-88741</span>
                    </div>
                    <div class="flex justify-between font-bold text-slate-900 text-base mt-2 pt-2 border-t border-slate-200">
                        <span>Amount Payable</span>
                        <span id="payment-amount-display">R 0.00</span>
                    </div>
                </div>

                <div class="space-y-3">
                    <button onclick="simulatePaymentSuccess()" class="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-3 rounded-xl cursor-pointer transition-all-300 text-sm">
                        Simulate Gateway Clearance (PayFast/Stripe Link)
                    </button>
                    <button onclick="switchView('dashboard')" class="w-full bg-slate-100 hover:bg-slate-200 text-slate-600 font-semibold py-2 rounded-xl cursor-pointer transition-all-300 text-xs">
                        Cancel Transaction
                    </button>
                </div>
            </div>
        </section>

        <!-- VIEW 3: LIVE INTERACTIVE AI COACHING SIMULATOR -->
        <section id="view-interview" class="hidden transition-all-300">
            <div class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden max-w-4xl mx-auto">
                <!-- Session Header Status -->
                <div class="bg-slate-900 p-4 text-white flex items-center justify-between">
                    <div class="flex items-center gap-3">
                        <span class="w-3 h-3 bg-emerald-500 rounded-full animate-ping"></span>
                        <h2 class="font-bold tracking-tight text-sm">Interactive AI Tutor Node Active</h2>
                    </div>
                    <span class="text-xs bg-slate-800 text-slate-400 px-3 py-1 rounded-md font-mono">Mode: 2026 corporate_matrix</span>
                </div>
                
                <!-- Chat Simulation Window -->
                <div id="chat-window" class="p-6 h-96 overflow-y-auto bg-slate-50 space-y-4">
                    <!-- Agent Starter Message -->
                    <div class="flex gap-3 max-w-2xl">
                        <div class="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center text-white font-bold text-xs shrink-0">AI</div>
                        <div class="bg-white border border-slate-200 p-4 rounded-xl rounded-tl-none shadow-xs text-sm">
                            Welcome to your elite preparatory workflow loop. I've integrated your CV configuration blueprint. Let's begin optimization: <strong>"Tell me about a highly complex technical conflict you resolved under severe deployment constraints."</strong>
                        </div>
                    </div>
                </div>

                <!-- Input Action Footer -->
                <div class="p-4 border-t border-slate-200 bg-white flex gap-3">
                    <input type="text" id="user-response-input" placeholder="Type your strategic behavioral or technical response response here..." class="flex-1 border border-slate-300 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-blue-500">
                    <button onclick="sendUserMessage()" class="bg-blue-600 hover:bg-blue-700 text-white font-bold px-6 py-3 rounded-xl text-sm transition-all-300 cursor-pointer">
                        Send Response
                    </button>
                </div>
            </div>
        </section>

    </main>

    <!-- STATE MANAGEMENT & INTERACTION SCRIPTS -->
    <script>
        // Global Cart and View States
        let cart = [];
        const dropZone = document.getElementById('drop-zone');
        const fileInput = document.getElementById('file-input');

        // Setup Drag & Drop Listeners
        if (dropZone) {
            dropZone.addEventListener('click', () => fileInput.click());
            dropZone.addEventListener('dragover', (e) => { e.preventDefault(); dropZone.classList.add('bg-slate-100'); });
            dropZone.addEventListener('dragleave', () => dropZone.classList.remove('bg-slate-100'));
            dropZone.addEventListener('drop', (e) => {
                e.preventDefault();
                dropZone.classList.remove('bg-slate-100');
                if (e.dataTransfer.files.length > 0) handleFileProcessing(e.dataTransfer.files[0]);
            });
        }

        function handleFileSelect(e) {
            if (e.target.files.length > 0) handleFileProcessing(e.target.files[0]);
        }

        function handleFileProcessing(file) {
            const metaDiv = document.getElementById('file-meta');
            metaDiv.innerText = `✓ Target Document Linked: ${file.name} (${(file.size/1024).toFixed(1)} KB)`;
            metaDiv.classList.remove('hidden');
        }

        // Cart Actions
        function addToCart(name, price) {
            if (cart.some(item => item.name === name)) return;
            cart.push({ name, price });
            renderCart();
        }

        function removeFromCart(name) {
            cart = cart.filter(item => item.name !== name);
            renderCart();
        }

        function renderCart() {
            document.getElementById('cart-count').innerText = cart.length;
            const ledgerItems = document.getElementById('cart-ledger-items');
            const checkoutBtn = document.getElementById('checkout-btn');
            
            if (cart.length === 0) {
                ledgerItems.innerHTML = '<p class="text-sm text-slate-400 italic">No operational optimization modules added yet.</p>';
                document.getElementById('ledger-subtotal').innerText = 'R 0.00';
                document.getElementById('ledger-vat').innerText = 'R 0.00';
                document.getElementById('ledger-total').innerText = 'R 0.00';
                checkoutBtn.className = "w-full mt-6 bg-slate-400 text-white font-bold py-3 rounded-xl cursor-not-allowed text-center text-sm";
                checkoutBtn.disabled = true;
                return;
            }

            let subtotal = cart.reduce((sum, item) => sum + item.price, 0);
            let vat = subtotal * 0.15; // 15% SARS VAT Constraint Mapping
            let total = subtotal + vat;

            ledgerItems.innerHTML = cart.map(item => `
                <div class="flex justify-between items-center bg-slate-50 p-3 rounded-lg border border-slate-100 text-sm">
                    <div>
                        <p class="font-bold text-slate-800">${item.name}</p>
                        <p class="text-xs text-blue-600 font-semibold">R ${item.price.toFixed(2)}</p>
                    </div>
                    <button onclick="removeFromCart('${item.name}')" class="text-slate-400 hover:text-red-500 text-xs font-bold cursor-pointer">Remove</button>
                </div>
            `).join('');

            document.getElementById('ledger-subtotal').innerText = `R ${subtotal.toFixed(2)}`;
            document.getElementById('ledger-vat').innerText = `R ${vat.toFixed(2)}`;
            document.getElementById('ledger-total').innerText = `R ${total.toFixed(2)}`;
            
            checkoutBtn.className = "w-full mt-6 bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded-xl cursor-pointer transition-all-300 text-center text-sm shadow-md shadow-blue-100";
            checkoutBtn.disabled = false;
        }

        // Smooth View Transitions
        function switchView(viewId) {
            ['dashboard', 'payment', 'interview'].forEach(view => {
                document.getElementById(`view-${view}`).classList.add('hidden');
            });
            document.getElementById(`view-${viewId}`).classList.remove('hidden');
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        function triggerCheckout() {
            const totalText = document.getElementById('ledger-total').innerText;
            document.getElementById('payment-amount-display').innerText = totalText;
            switchView('payment');
        }

        function simulatePaymentSuccess() {
            alert("Payment processed securely through compliance factory layer. Transitioning to active coaching environment node...");
            switchView('interview');
        }

        // Chat Interaction Processing
        function sendUserMessage() {
            const input = document.getElementById('user-response-input');
            const text = input.value.trim();
            if (!text) return;

            const chatWindow = document.getElementById('chat-window');
            
            // Append User Line Text
            chatWindow.innerHTML += `
                <div class="flex gap-3 max-w-2xl ml-auto justify-end">
                    <div class="bg-blue-50 border border-blue-100 p-4 rounded-xl rounded-tr-none shadow-xs text-sm text-slate-800">
                        ${text}
                    </div>
                </div>
            `;
            
            input.value = "";
            chatWindow.scrollTop = chatWindow.scrollHeight;

            // Generate Simulated Immediate AI Evaluative Response Loop
            setTimeout(() => {
                chatWindow.innerHTML += `
                    <div class="flex gap-3 max-w-2xl">
                        <div class="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center text-white font-bold text-xs shrink-0">AI</div>
                        <div class="bg-white border border-slate-200 p-4 rounded-xl rounded-tl-none shadow-xs text-sm">
                            <strong>[Evaluation Return Matrix]</strong> Score Allocation metrics matched: 84%. Excellent structural context mapping. However, remember your 2026 corporate hybrid presentation rules: keep technical focus clean and emphasize direct outcome data keys explicitly.
                        </div>
                    </div>
                `;
                chatWindow.scrollTop = chatWindow.scrollHeight;
            }, 1200);
        }
    </script>
</body>
</html>
