let showAllBtn = document.getElementById("btn");
let countryFeild = document.getElementById("CountryFeild");
var searchCountry =  document.getElementById("search_button");
let addCountry = document.getElementById("add_button")
let deleteCountry = document.getElementById("delete_button");

searchCountry.addEventListener("click",function(){
    let searchInput =  document.getElementById("search_input").value;

    country = $.get("/Countries/" + searchInput,function(response){
        let country = JSON.parse(response);
        console.log(country.name);
    }).fail(function(){
        console.log("I Failed")
    });
});


showAllBtn.addEventListener("click",function(){

    country = $.get("/Countries",function(response){
        let country = JSON.parse(response);
         console.log(country.name);
    });
 });
 
deleteCountry.addEventListener("click",function(){
    let countryToRemove = document.getElementById("delete_input");
    $.ajax({
        url:"/Countries/"+countryToRemove,
        type: 'DELETE',
        success: function(result){
            console.log("Removed");
        },
        statusCode: {
            400: function(){
                console.log("Country not found")
            }
        }
    });
});

addCountry.addEventListener("click",function(){
    let countryToAdd = document.getElementById("add_input").value;
    $.post("/Countries/"+countryToAdd,function(){
        console.log("Added " + countryToAdd + " to DB");
    }).fail(function(){
        console.log("Country already in database");
    });
});