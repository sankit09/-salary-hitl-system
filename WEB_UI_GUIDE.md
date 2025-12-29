# Web UI Quick Start Guide

## 🚀 Run the Web UI (Alternative to Streamlit)

If Streamlit is not working, use the Flask-based web UI instead:

### 1. Install Flask (if not already installed)
```bash
pip install flask
```

### 2. Start the Web Server
```bash
python web_app.py
```

### 3. Open in Browser
Navigate to: **http://localhost:5000**

---

## ✨ Features

✅ **Beautiful gradient UI** - Modern, professional design  
✅ **Responsive layout** - Works on all screen sizes  
✅ **Interactive cards** - Click to select departments  
✅ **Same HITL workflow** - Identical functionality to Streamlit  
✅ **Live updates** - No page refreshes needed  

---

## 📺 How to Use

1. **Select Department** - Click on any department card
2. **Analyze** - Click "Analyze Department" button
3. **Review Proposal** - See highest-paid employee and AI proposal
4. **Make Decision**:
   - Click **✅ Approve** to accept
   - Click **❌ Reject** to decline
   - Click **📝 Modify** to change values
5. **View Result** - See the outcome and start new analysis

---

## 🎨 UI Design

- **Purple gradient header** - Professional look
- **Card-based selection** - Easy to use
- **Color-coded results**:
  - Green = Approved
  - Red = Rejected
  - Yellow = Modified
- **Smooth animations** - Hover effects and transitions
- **Clean typography** - Easy to read

---

## 🔧 Technical Details

- **Backend**: Flask (Python web framework)
- **Frontend**: HTML + CSS + Vanilla JavaScript
- **No external dependencies**: All CSS/JS embedded
- **Port**: 5000 (default)
- **Sessions**: Maintains workflow state

---

## ⚡ Advantages Over Streamlit

✅ Lighter weight - No heavy dependencies  
✅ More control - Custom HTML/CSS  
✅ Faster startup - Simpler framework  
✅ Standard web tech - Easy to customize  
✅ Works anywhere - More compatible  

---

## 🛠️ Customize

Edit `templates/index.html` to:
- Change colors (search for `#667eea` and `#764ba2`)
- Modify layout
- Add new sections
- Update styling

---

Happy coding! 🎉
