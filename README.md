# **Finnish Wikipedia Articles (20.02.2025) - JSON Dataset**  

On my journey towards building my first **small Finnish cognitive intelligence model**, the first step was to **parse the entire Finnish Wikipedia** in a structured way.  

I believe the **end result is quite solid**.  

There are **some inaccuracies** in the dataset, but **95% of it is in good Finnish and structurally sound**.  

---

## **Instructions for Extracting Finnish Wikipedia**
Follow these steps to **convert Finnish Wikipedia into a structured JSON dataset**.

### **1. Download the latest Wikipedia dump**
Get the latest **Finnish Wikipedia dump file** from:  
🔗 [https://dumps.wikimedia.org/fiwiki/](https://dumps.wikimedia.org/fiwiki/)  

---

### **2. Extract the Wikipedia XML file**
After downloading, extract the file. You will get a **large `.xml` file**.  

---

### **3. Adjust the configuration in `wiki_to_text.py`**
Open the script **`wiki_to_text.py`** and update the **file path** inside the script.

Modify the following line:  

```python
wiki_xml_file = 'xml.xml'  # Update this to match your extracted file
```

---

### **4. Run the script**
Execute the script from the **command line**:  

```bash
python wiki_to_text.py
```

---

### **5. Grab Some Coffee ☕**
Processing the Wikipedia dump **takes time**, so **sit back and enjoy a few cups of coffee** while it runs.  

---

### **5. Grab Some Coffee ☕**
Processing the Wikipedia dump **takes time**, so **sit back and enjoy a few cups of coffee** while it runs.  

---

## **Big Thanks to David Shapiro!**
A **huge thank you** to **David Shapiro** for providing **nearly finished code** that helped streamline this project.  

🔗 **GitHub Repo:** [daveshap/PlainTextWikipedia](https://github.com/daveshap/PlainTextWikipedia) 
