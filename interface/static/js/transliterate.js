const select = document.getElementById('scriptSelect');

// Update select options from object properties
function updateSelectFromObject(selectElement, obj) {
    // Clear existing options
    selectElement.innerHTML = '';
    
    // Create options from object properties
    Object.keys(obj).forEach(key => {
        const optionElement = document.createElement('option');
        optionElement.value = key;
        optionElement.textContent = key;
        selectElement.appendChild(optionElement);
    });
}

// Callback function that handles the change
function handleSelectChange(event) {
    const newScript = event.target.value;

    const nodeList = document.querySelectorAll(".align-text");

    for(const elem of nodeList) {
        elem.innerHTML = Sanscript.t(elem.innerHTML, previousScript, newScript);
    }
    // Update the previous value for next time
    previousScript = newScript;
}

updateSelectFromObject(select, Sanscript.schemes);
select.value = "devanagari";

// Store the previous value
let previousScript = select.value;
// Add event listener to the select element
select.addEventListener('change', handleSelectChange);

