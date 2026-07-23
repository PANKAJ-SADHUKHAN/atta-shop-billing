if ("serviceWorker" in navigator) {

    navigator.serviceWorker.register("/static/sw.js")

    .then(() => {

        console.log("Service Worker Registered");

    });

}

    const SHOP_NAME = "Sadhukhan Enterprise";

    const SHOP_ADDRESS =
    "45 RNT Path, Titagarh, Laxmighat";

    const SHOP_PHONE =
    "9830747515";
    const DEVICE_TOKEN =
    "ATTA_SHOP_2026_SECRET";


function setQty(value){

    document.getElementById("qty").value = value;
    document.querySelectorAll(".quick-buttons button")
        .forEach(btn => btn.classList.remove("active"));

    event.target.classList.add("active");
}
 function clearQuickSelection(){

    document.querySelectorAll(".quick-buttons button")
        .forEach(btn => btn.classList.remove("active"));

}

function formatBillId(id){

    return String(id).padStart(4, "0");

}

function formatQuantity(qty){

    qty = parseFloat(qty);

    const kg = Math.floor(qty);

    const grams = Math.round(
        (qty - kg) * 1000
    );

    if(grams === 0){
        return `${kg} KG`;
    }

    if(kg === 0){
        return `${grams} G`;
    }

    return `${kg} . ${grams} G`;
}


async function generateBill(){

    let shopName = SHOP_NAME;

    let address = SHOP_ADDRESS;

    let phone = SHOP_PHONE;
    const billId = await saveBillToServer();
    let qty = document.getElementById("qty").value;
    if(qty === ""){

        alert("Please enter the quantity.");

        document.getElementById("qty").focus();

        return;
    }

    let now = new Date();
    const dateTime = now.toLocaleString("en-IN", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    hour12: true
});
    

    document.getElementById("receipt").innerHTML = `
    <div class="bill-print">
        <p><b>Bill No:</b> ${formatBillId(billId)}</p>
        <h3>${shopName}</h3>
        <p>${address}</p>
        <p>Phone: ${phone}</p>
        <hr class="receipt-line">
        <p>Date: ${dateTime}</p>
        <hr class="receipt-line">
        <div class="grid-container">
        <div class="item-name shared-style">ATTA</div>
        <div class="qty-big shared-style">${formatQuantity(qty)}</div>
        </div>
        <hr class="receipt-line">
        <p>Thank You</p>

    </div>
`;
}
function clearBill(){

    document.getElementById("receipt").innerHTML = "";

    document.getElementById("qty").value = "";

    document.getElementById("qty").focus();

}
async function saveBillToServer() {

    console.log("Saving bill...");

    const qty = document.getElementById("qty").value;

    const response = await fetch("/api/bill", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            quantity: qty,
            device_token: DEVICE_TOKEN
        })
    });

    const result = await response.json();

    console.log(result);
    return result.bill_id;
}
