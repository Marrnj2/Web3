let showAllBtn = document.getElementById("btn");
let countryFeild = document.getElementById("CountryFeild");
var xhttp  = new XMLHttpRequest();

showAllBtn.addEventListener("click",function(){


   country = $.get("/Countries",function(response){
       let country = JSON.parse(response);
        renderHTML(country);
   });
});

function renderHTML(country){
    let htmlString = "";

        let text = 
        htmlString += "<p>" + country[0].name + "</p>";
    
    countryFeild.insertAdjacentHTML('beforeend',htmlString);
}