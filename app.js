import express from "express";

const app = express();

app.get("/", (req, res) => {
  res.send("HELLOWWWW");
});

app.get("/animal", (req, res) => {
  res.send("SANDEEP REDDY MASS");
});

app.listen(8000, () => {
  console.log("helloooow");
});
