var ugibiDOM = document.getElementById("ugibi");
var gumbiDOM = document.getElementById("buttons");
var hangedDOM = document.getElementById("hanged");

var besede = ["testing", "test"];


var beseda;
var poskusi = 0;
const maxZgresitev = 6;
var ugibi = [];

init();
newGame();

function init(){
    gumbiDOM.childNodes.forEach((ele) => {
        ele.addEventListener("click", () => {
            vnosCrke(ele.textContent);
        });
    });
}

function newGame(){
    poskusi = 0;
    beseda = besede[Math.floor(Math.random()*besede.length)];
    ugibi = [];
    for (let i = 0; i < beseda.length; i++) {
        ugibi.push("&nbsp;");
    }
    nextImg(true);
    updateUgibi();
}

function vnosCrke(crka){

    let uganil = false;

    for (let i in beseda) {
        if(beseda[i].toUpperCase() === crka.toUpperCase()) {
            ugibi[i] = crka;
            uganil = true;
        }
    }

    if(!uganil){
        poskusi++;
        if(poskusi >= maxZgresitev) {
            nextImg();
            setTimeout(() => {
                alert("GAME OVER");
                newGame();
            }, 50);
        } else nextImg();
    } else {
        updateUgibi();
        if(ugibi.indexOf("&nbsp;") === -1){
            setTimeout(() => {
                alert("ZMAGAL SI!");
                newGame();
            }, 50)

        }
    }

}

function updateUgibi(){
    ugibiDOM.innerHTML = "";
    for (let i in ugibi) {
        ugibiDOM.innerHTML += `<span>${ugibi[i]}</span>`;
    }
}

function nextImg(reset=false){
    let imgNum = Number.parseInt(hangedDOM.src.split('.')[0].split('_')[1]) + 1;
    if(reset){
        imgNum = -1
    }
    hangedDOM.src = `media/hanged_${imgNum}.svg`;
}


