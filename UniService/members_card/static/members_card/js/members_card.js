const iMin = 0
const iMax = 7
var iEntered = 0

async function limit_input() {
    iEntered = document.getElementById("txtMemberNo").value.length
    if (iEntered == iMax) {
        const sid = document.getElementById("txtMemberNo").value
        document.getElementById("txtFName").focus();
        const user = await fetch(`/enroll/api/user/${sid}/`)
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
        const usercards = await member_cards(sid)
        let usercard;
        let image = user.image
        for (let i in usercards["results"]) {
            if (usercards["results"][i].active) {
                usercard = usercards["results"][i];
                break
            }
        }
        if (!usercard) {
            console.error("No User Card")
            const issue = new Date()
            const expiry = new Date()
            expiry.setMonth(12, 0)
            usercard = {
                issued_date: issue.toISOString().slice(0, 10),
                expiry_date: expiry.toISOString().slice(0, 10),
                photo: null
            }
        }

        image = usercard.photo ? usercard.photo : image

        //Fill the text fields with a fetch here
        var FName = document.getElementById("txtFName");
        FName.value = user.first_name;
        var LName = document.getElementById("txtLName");
        LName.value = user.last_name;
        showSelection(
            user.id,
            user.first_name,
            user.last_name,
            image,
            usercard.issued_date,
            usercard.expiry_date,
            usercard.card_num
        );
    }
    var counterSpan = document.getElementById("counterHolder");
    counterSpan.innerHTML = iEntered;
}

async function member_cards(sid) {
    return fetch(`/enroll/api/card/?user_id=${sid}`)
        .then((response) => {
            if (response.ok) {
                // console.log(response.json())
                return response.json()
            } else {
                throw new Error(`User has never been issued a card: ${sid}`)
            }
        })
        .catch((err) => {
            console.error(err);
        })
}

function ChangePic(income) {
    var fileupload = document.getElementById("FileUpload");
    var filePath = document.getElementById("spnFilePath");
    var button = document.getElementById("btnChoose");
    //var fileName = income.value;
    var fileName = income.value.split('\\')[income.value.split('\\').length - 1];
    filePath.innerHTML = "<b>Selected File: </b>" + fileName;
    limit_input();
    showSelection();
    document.getElementById("photo").src = fileName;
}

async function saveSelection(expiry = `${new Date().getFullYear()}-12-31`) {
    const member_id = document.getElementById("cardmember").innerText;
    console.log(member_id)
    if (!member_id) {
        return
    }
    const cardsData = await member_cards(member_id);
    const cards = cardsData["results"]
    const auth = `Basic ${btoa(member_id + ':testing124')}`
    for (let i in cards) {
        if (cards[i].active) {
            console.log(cards[i].card_num)
            const request_body = JSON.stringify({ "active": false })
            console.log(request_body.length)
            fetch(`/enroll/api/card/${cards[i].card_num}/`, {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json",
                    "Connection": "keep-alive",
                    "Content-Length": request_body.length,
                    "Authorization": auth
                },
                body: request_body
            }).catch(err => console.error(err))
        }
    }
    let photo = localStorage.getItem("current_photo");
    if (!photo) {
        return
    }
    // if (photo){

    // }
    const request_body = JSON.stringify({
        expiry_date: expiry,
        active: true,
        photo: photo,
        user_id: member_id
    })
    console.log(photo)
    const cardRequest = new Request(
        "/enroll/api/card/",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Connection": "keep-alive",
                "Content-Length": request_body.length,
                "Authorization": auth
            },
            body: request_body
        }
    )
    fetch(cardRequest)
        .then(response => {
            if (response.ok) {
                alert("Card has been successfully requested.")
            } else {
                alert("Request failed. Contact enrollment if issue persists.")
            }
            return response.json()
        })
        .catch(err => console.error(err))
}

function showSelection(sid, firstname, lastname, img, issue, expire, card_num) {
    localStorage.setItem("current_photo", img);
    document.getElementById("cardmember").innerText = sid;
    document.getElementById("cardname").innerText = `${firstname} ${lastname}`;
    document.getElementById("cardex").innerHTML = expiryString(issue, expire);
    // deepcode ignore DOMXSS: This is validated elsewhere.
    document.getElementById("inputdata").innerHTML = DrawCode39Barcode(`${sid}${card_num}`, 0);
    document.getElementById("overlay").src = "/enroll/static/members_card/images/sample_stamp.png"
    document.getElementById("imagePreview").style = style = "background-image: url(" + img + ");"
}
function expiryString(issue, expire) {
    return `<p class="rightAligned">Issued: ${new Date(issue).toLocaleDateString()}<br />
Expiry: ${new Date(expire).toLocaleDateString()}</p>`
}

function DrawCode39Barcode(data, checkDigit) {
    return DrawHTMLBarcode_Code39(
        data,
        checkDigit,
        "yes",
        "cm",
        0,
        6,
        1,
        3,
        "bottom",
        "center",
        "",
        "black",
        "white",);
}
function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
            $('#imagePreview').hide();
            $('#imagePreview').fadeIn(650);
            localStorage.setItem("current_photo", e.target.result);
        };
        reader.readAsDataURL(input.files[0]);
    }
}
$("#imageUpload").change(function () {
    readURL(this);
});
limit_input();
