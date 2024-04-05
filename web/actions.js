
/*
  Show and hide proofs
*/
function proofToggle(idx){
    var toggler = document.getElementById("toggleproof" + idx);
    var proof = document.getElementById("proof" + idx);
    if (toggler.innerText == "[Hide Proof]"){
        proof.style = "display: none;";
        toggler.innerText = "[Show Proof]";
    }
    else{
        proof.style = "display: block;";
        toggler.innerText = "[Hide Proof]";
    }
}


function allProofShow(){
    var proofs = document.getElementsByClassName("proof");
    for(var i = 0, size = proofs.length; i < size ; i++){
        var prf = proofs[i];
        var toggler = document.getElementById("toggle" + prf.id);
        prf.style = "display: block;";
        toggler.innerHTML = "[Hide Proof]";
    }
}


function allProofHide(){
    var proofs = document.getElementsByClassName("proof");
    for(var i = 0, size = proofs.length; i < size ; i++){
        var prf = proofs[i];
        var toggler = document.getElementById("toggle" + prf.id);
        prf.style = "display: none;";
        toggler.innerHTML = "[Show Proof]";
    }
}



/*
  Show and hide SOS files
*/
function toggleFile(fname){
    var toggler = document.getElementById("toggle" + fname);
    var file = document.getElementById(fname);
    if (toggler.innerHTML == "[Reduce File]"){
        file.style = "max-height: 105px;";
        toggler.innerHTML = "[Expand File]";
    }
    else{
        file.style = "";
        toggler.innerHTML = "[Reduce File]";
    }
}
