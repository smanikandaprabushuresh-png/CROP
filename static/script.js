// Script for Crop Recommendation System

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("cropForm");
    
    // Sample presets for quick testing and student demonstration
    const presets = {
        rice: {
            nitrogen: 80,
            phosphorus: 48,
            potassium: 40,
            temperature: 24,
            humidity: 82,
            ph: 6.5,
            rainfall: 240
        },
        maize: {
            nitrogen: 78,
            phosphorus: 45,
            potassium: 20,
            temperature: 22,
            humidity: 65,
            ph: 6.2,
            rainfall: 85
        },
        chickpea: {
            nitrogen: 40,
            phosphorus: 68,
            potassium: 80,
            temperature: 19,
            humidity: 17,
            ph: 7.2,
            rainfall: 80
        },
        coffee: {
            nitrogen: 100,
            phosphorus: 28,
            potassium: 30,
            temperature: 25,
            humidity: 60,
            ph: 6.8,
            rainfall: 155
        }
    };

    // Attach click listeners to preset buttons
    const presetButtons = document.querySelectorAll(".btn-preset");
    presetButtons.forEach(button => {
        button.addEventListener("click", function () {
            const cropType = this.getAttribute("data-preset");
            const data = presets[cropType];
            if (data) {
                document.getElementById("nitrogen").value = data.nitrogen;
                document.getElementById("phosphorus").value = data.phosphorus;
                document.getElementById("potassium").value = data.potassium;
                document.getElementById("temperature").value = data.temperature;
                document.getElementById("humidity").value = data.humidity;
                document.getElementById("ph").value = data.ph;
                document.getElementById("rainfall").value = data.rainfall;
            }
        });
    });

    // Form validation
    if (form) {
        form.addEventListener("submit", function (e) {
            const fields = [
                { id: "nitrogen", name: "Nitrogen (N)", min: 0, max: 200 },
                { id: "phosphorus", name: "Phosphorus (P)", min: 0, max: 200 },
                { id: "potassium", name: "Potassium (K)", min: 0, max: 250 },
                { id: "temperature", name: "Temperature", min: 0, max: 60 },
                { id: "humidity", name: "Humidity", min: 0, max: 100 },
                { id: "ph", name: "Soil pH", min: 0, max: 14 },
                { id: "rainfall", name: "Rainfall", min: 0, max: 500 }
            ];

            for (let f of fields) {
                const input = document.getElementById(f.id);
                const val = parseFloat(input.value);

                if (isNaN(val)) {
                    alert("Please enter a valid number for " + f.name);
                    input.focus();
                    e.preventDefault();
                    return false;
                }

                if (val < f.min || val > f.max) {
                    alert(f.name + " must be between " + f.min + " and " + f.max + ".");
                    input.focus();
                    e.preventDefault();
                    return false;
                }
            }

            return true;
        });
    }
});
