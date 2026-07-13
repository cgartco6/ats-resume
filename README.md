# Sovereign Career Engine 🚀

A highly responsive, automated AI Career and Enterprise system designed to build, compile, and run entirely on modern cloud free tiers.

## 📐 Free-Tier Architecture Blueprint

1. **Frontend Deployment (Vercel / Netlify)**
   - The reactive web portal resides entirely within `public/index.html`. 
   - Because it runs completely on client-side state engines, it can be hosted **100% Free Forever** on Netlify or Vercel static hosting drops.

2. **Backend & Compilation (GitHub Codespaces / Local Machine)**
   - The native `builder.py` and `engineering_prompt.py` systems run locally or within a free GitHub Codespace container.
   - Leverages the free tier API keys to process documents and generate production code modules without infrastructure charges.

## 🚀 Step-by-Step Deployment Protocol

### Phase A: Launching the Frontend UI
* **On Netlify:** Drag and drop the `public` folder directly onto the Netlify drop dashboard.
* **On Vercel:** Initialize via terminal: `vercel deploy` selecting the `public` directory as your distribution root.

### Phase B: Compiling System Modules Locally
1. Clone this repository to your machine.
2. Initialize your free token key via terminal:
   ```bash
   export GEMINI_API_KEY="your_free_gemini_api_key"
