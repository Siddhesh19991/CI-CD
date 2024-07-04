window.onload = function () {
  populateMunicipalities();
  updateFormFields();
};

var municipalities = [
  "Stockholm",
  "Göteborg",
  "Malm",
  "Uppsal",
  "Linköping",
  "Nack",
  "Soln",
  "Västerå",
  "Täb",
  "Örebr",
  "Norrtälj",
  "Helsingborg",
  "Lund",
  "Järfäll",
  "Sundsvall",
  "Sundbyberg",
  "Hudding",
  "Haning",
  "Gävl",
  "Jönköping",
  "Liding",
  "Sollentun",
  "Värmd",
  "Norrköping",
  "Karlstad",
  "Uddevall",
  "Ume",
  "Kalma",
  "Trelleborg",
  "Mölndal",
  "Kungsback",
  "Halmstad",
  "Skellefte",
  "Lule",
  "Eskilstun",
  "Österåker",
  "Borå",
  "Varberg",
  "Södertälj",
  "Borläng",
  "Ystad",
  "Vänersborg",
  "Strängnä",
  "Trollhättan",
  "Sandviken",
  "Kungälv",
  "Härnösand",
  "Tyres",
  "Al",
  "Botkyrk",
  "Växj",
  "Danderyd",
  "Velling",
  "Karlskron",
  "Sigtun",
  "Sjöb",
  "Kristianstad",
  "Lidköping",
  "Pite",
  "Falkenberg",
  "Staffanstorp",
  "Örnsköldsvik",
  "Svedal",
  "Ängelholm",
  "Skövd",
  "Arvik",
  "Östersund",
  "UpplandsVäsb",
  "Klippan",
  "Fal",
  "Lerum",
  "Falköping",
  "Enköping",
  "Nyköping",
  "Eker",
  "Alingså",
  "Gotland",
  "Motal",
  "Sal",
  "Västervik",
  "Oxelösund",
  "Timr",
  "Värnam",
  "Vallentun",
  "Hudiksvall",
  "Östhammar",
  "Boden",
  "Hässleholm",
  "Arbog",
  "Söderhamn",
  "Skurup",
  "Karlshamn",
  "Tros",
  "Avest",
  "Kävling",
  "Karlskog",
  "Nynäshamn",
  "Hab",
  "Ulricehamn",
  "Mark",
  "Oskarshamn",
  "Orus",
  "Torsb",
  "Kristinehamn",
  "Heb",
  "LillaEdet",
  "ÖstraGöing",
  "Landskron",
  "Hammar",
  "Smedjebacken",
  "Nässj",
  "Katrineholm",
  "Hofor",
  "Tidaholm",
  "Ronneb",
  "Säffl",
  "Sunn",
  "Höganä",
  "Eslöv",
  "Hallsberg",
  "Surahammar",
  "Härryd",
  "Tranem",
  "Öcker",
  "Mjölb",
  "Laholm",
  "Lekeberg",
  "Vårgård",
  "Kil",
  "Vaxholm",
  "Ljungb",
  "Bjuv",
  "Lomm",
  "Ludvik",
  "Torså",
  "Bollnä",
  "Strömstad",
  "Bromöll",
  "År",
  "Borgholm",
  "Kramfor",
  "Tomelill",
  "Tjörn",
  "Alvest",
  "Vännä",
  "Vetland",
  "Sölvesborg",
  "Upplands-Bro",
  "Ång",
  "Tierp",
  "Svalöv",
  "Boxholm",
  "Örkelljung",
  "Älmhult",
  "Strömsund",
  "Haparand",
  "Emmabod",
  "Mor",
  "Kali",
  "Karlsborg",
  "Grästorp",
  "Mörbylång",
  "Mönsterå",
  "Kirun",
  "Finspång",
  "Olofström",
  "Forshag",
  "Kungsör",
  "Stenungsund",
  "Lesseb",
  "Ljusdal",
  "Gagnef",
  "Hagfor",
  "Gällivar",
  "Osb",
  "Essung",
  "Partill",
  "Härjedalen",
  "Hylt",
  "Skar",
  "Hallstahammar",
  "Simrishamn",
  "Salem",
  "Grum",
  "Hedemor",
  "Vingåker",
  "Bengtsfor",
  "Herrljung",
  "Leksand",
  "Askersund",
  "Hj",
  "Årjäng",
  "Knivst",
  "Hällefor",
  "Höör",
  "Åtvidaberg",
  "Älvkarleb",
  "Gnosj",
  "Åstorp",
  "Vimmerb",
  "Vadsten",
  "Lindesberg",
  "Var",
  "Skinnskatteberg",
  "Fagerst",
  "Söderköping",
  "Båstad",
  "S",
  "Tanum",
  "Tibr",
  "Rättvik",
  "Perstorp",
  "Tingsryd",
  "Ockelb",
  "Nykvarn",
  "Nybr",
  "Tranå",
  "Burlöv",
  "Nordanstig",
  "Nor",
  "Törebod",
  "Filipstad",
  "Mariestad",
  "Lysekil",
  "Uppviding",
  "Vaggeryd",
  "Valdemarsvik",
  "Färgeland",
  "Övertorne",
];

function populateMunicipalities() {
  var datalist = document.getElementById("municipalities");

  municipalities.forEach(function (municipality) {
    var option = document.createElement("option");
    option.value = municipality;
    datalist.appendChild(option);
  });
}

function updateFormFields() {
  document.getElementById("pred_value").textContent = "";
  var houseType = document.getElementById("houseType").value;
  var commonFields = document.getElementById("common-fields");
  var lagenhetFields = document.getElementById("lagenhet-fields");
  var nonLagenhetFields = document.getElementById("non-lagenhet-fields");

  // Hide all fields initially
  commonFields.style.display = "none";
  lagenhetFields.style.display = "none";
  nonLagenhetFields.style.display = "none";

  // Show common fields for all house types except the default empty option
  if (houseType) {
    commonFields.style.display = "block";

    if (houseType === "Lägenhet") {
      lagenhetFields.style.display = "block";
    } else {
      nonLagenhetFields.style.display = "block";
    }
  }
}

function prediction() {
  document.getElementById("pred_value").textContent = "";
  var municipalityInput = document.getElementById("municipality").value.trim();

  var municipalityError = document.getElementById("municipalityError");
  municipalityError.textContent = "";

  if (!municipalities.includes(municipalityInput)) {
    municipalityError.textContent =
      "Please select a valid Municipality from the list.";
    return;
  }

  // Validate Living Area
  var livingAreaInput = parseFloat(
    document.getElementById("living_area").value
  );
  var livingAreaError = document.getElementById("livingAreaError");
  livingAreaError.textContent = "";

  if (isNaN(livingAreaInput) || livingAreaInput <= 0) {
    livingAreaError.textContent =
      "Living Area must be a positive number greater than 0.";
    return;
  }

  //Validate rooms
  var houseType = document.getElementById("houseType").value;
  var roomError = document.getElementById("roomError");
  roomError.textContent = "";

  if (houseType === "Lägenhet") {
    var roomInput = parseFloat(document.getElementById("rooms").value);
    if (isNaN(roomInput) || roomInput < 0) {
      roomError.textContent = "Rooms must be a non-negative number (can be 0).";
      return;
    }
  }

  // Validate Plot Area
  var plotAreaInput = parseFloat(document.getElementById("plot_area").value);
  var plotAreaError = document.getElementById("plotAreaError");
  plotAreaError.textContent = "";

  if (houseType != "Lägenhet") {
    if (isNaN(plotAreaInput) || plotAreaInput < 0) {
      plotAreaError.textContent =
        "Plot Area must be a non-negative number (can be 0).";
      return;
    }
  }

  // Validate Other Area
  var otherAreaInput = parseFloat(document.getElementById("other_area").value);
  var otherAreaError = document.getElementById("otherAreaError");
  otherAreaError.textContent = "";

  if (houseType != "Lägenhet") {
    if (isNaN(otherAreaInput) || otherAreaInput < 0) {
      otherAreaError.textContent =
        "Other Area must be a non-negative number (can be 0).";
      return;
    }
  }

  let xmlr = new XMLHttpRequest();
  xmlr.open("POST", "/predict", true);

  xmlr.setRequestHeader("Content-Type", "application/json;charset = utf-8");

  xmlr.onreadystatechange = function () {
    if (xmlr.readyState == 4) {
      if (xmlr.status == 200) {
        let jsonResponse = JSON.parse(xmlr.responseText);
        document.getElementById("pred_value").textContent =
          jsonResponse.value + " million in Kr";
        console.log("Success");
      } else {
        console.error("Error");
      }
    }
  };

  var formData = {
    House_Type: document.getElementById("houseType").value,
    Municipality: document.getElementById("municipality").value,
    Living_Area: document.getElementById("living_area").value,
    Built_On: document.getElementById("built_on").value,
    Rooms: document.getElementById("rooms").value,
    Lift: document.getElementById("lift").value,
    Balcony: document.getElementById("balcony").value,
    Plot_Area: document.getElementById("plot_area").value,
    Other_Area: document.getElementById("other_area").value,
  };

  xmlr.send(JSON.stringify(formData));
}
