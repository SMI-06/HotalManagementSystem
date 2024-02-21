let countries = [
    {
        countryName: "Pakistan"
    },
    {
        countryName: "Canada"
    },
    {
        countryName: "Germany"
    }
]

let cities = [
    {
        citiesName: "Karachi"
    },
    {
        citiesName: "Lahore"
    },
    {
        citiesName: "Islamabad"
    },
    {
        citiesName: "Quetta"
    },
    {
        citiesName: "Peshawar"
    },
]


for (let i = 0; i < countries.length; i++) {
    document.querySelector("#country").innerHTML +=
        `<option value="${countries[i].countryName}">${countries[i].countryName}</option>`
}
for (let i = 0; i < cities.length; i++) {
    document.querySelector("#cities").innerHTML +=
        `<option value="${cities[i].citiesName}">${cities[i].citiesName}</option>`
}