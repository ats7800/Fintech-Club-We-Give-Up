let selectedBtn = "Apple";
let loading = false;

const buttons = document.getElementsByClassName("stock-button");
const submitBtn = document.getElementById("submitBtn");

submitBtn.addEventListener("click", function () {
  date = document.getElementById("date").value;
  const data = {
    date: date,
    stock: selectedBtn,
  };
  postPredict(data);
});

// document.addEventListener("click", function () {
//   senti = sentiArea.value;
//   const data = {
//     senti: senti,
//   };
//   sentiPredict(data);
// });

for (let i = 0; i < buttons.length; i++) {
  buttons[i].addEventListener("click", function () {
    // Remove active class from all buttons
    for (let j = 0; j < buttons.length; j++) {
      buttons[j].classList.remove("active");
    }
    // Add active class to the clicked button
    this.classList.add("active");
    selectedBtn = this.name;
    // console.log(this.name);
  });
}

function postPredict(data) {
  if (loading) return;
  loading = true;
  document.getElementById("loadingIcon").style.display = "inline-block";
  fetch("http://localhost:5000/submit", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Response from server:", data);
      document.getElementById("loadingIcon").style.display = "none";
      loading = false;
    })
    .catch((error) => {
      console.error("Error:", error);
      document.getElementById("loadingIcon").style.display = "none";
      loading = false;
    });
}
