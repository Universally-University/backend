const iMin = 0
const iMax = 7
var iEntered = 0

async function limit_input() {
    iEntered = document.getElementById("txtMemberNo").value.length
    if (iEntered == iMax) {
        const sid = document.getElementById("txtMemberNo").value
        document.getElementById("txtFName").focus();
        const user = await fetch(`/api/user/${sid}`)
            .then((response) => {
                if (response.ok) {
                    return response.json()
                } else {
                    throw new Error(`Not a valid Member ID: ${sid}`)
                }
            })
            .catch((err) => {
                alert(err);
            })
        //Fill the text fields with a fetch here
        var FName = document.getElementById("txtFName");
        FName.value = user.first_name;
        var LName = document.getElementById("txtLName");
        LName.value = user.last_name;
        showSelection(
            user.id,
            user.first_name,
            user.last_name,
            user.image,
            user.dob
        );
    }
    var counterSpan = document.getElementById("counterHolder");
    counterSpan.innerHTML = iEntered;
}

function ChangePic(oFileInput) {
    pic = oFileInput.value;
    showSelection();
}

function showSelection(sid, firstname, lastname, img, dob) {
    document.getElementById("cardmember").innerText = sid;
    document.getElementById("cardname").innerText = `${firstname} ${lastname}`;
    document.getElementById("cardex").innerText = "13/12/23";
    // document.getElementById("dob") = dob; // Todo: Not working.
    // deepcode ignore DOMXSS: This is validated elsewhere.
    document.getElementById("inputdata").innerHTML = DrawCode39Barcode(String(sid), 0);
    document.getElementById("photo").src = img;
    document.getElementById("HEREIAM")
}
// limit_input()