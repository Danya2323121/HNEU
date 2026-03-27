const express = require("express");
const bodyParser = require("body-parser");
const jwt = require("jsonwebtoken");

const app = express();
app.use(bodyParser.json());

const SECRET = "secret123";

let books = [
    { isbn: "1", title: "Book One", author: "Author A", reviews: [] },
    { isbn: "2", title: "Book Two", author: "Author B", reviews: [] }
];

let users = [];

app.get("/books", (req, res) => {
    res.json(books);
});

app.get("/books/isbn/:isbn", (req, res) => {
    const book = books.find(b => b.isbn === req.params.isbn);
    res.json(book || "Not found");
});

app.get("/books/author/:author", (req, res) => {
    const result = books.filter(b => b.author === req.params.author);
    res.json(result);
});

app.get("/books/title/:title", (req, res) => {
    const result = books.filter(b => b.title === req.params.title);
    res.json(result);
});

app.get("/books/review/:isbn", (req, res) => {
    const book = books.find(b => b.isbn === req.params.isbn);
    res.json(book ? book.reviews : []);
});

app.post("/register", (req, res) => {
    users.push(req.body);
    res.json("User registered");
});

app.post("/login", (req, res) => {
    const user = users.find(u => u.username === req.body.username);
    if (user) {
        const token = jwt.sign({ username: user.username }, SECRET);
        res.json({ token });
    } else {
        res.status(401).json("Invalid user");
    }
});

function auth(req, res, next) {
    const token = req.headers.authorization;
    if (!token) return res.sendStatus(403);

    try {
        jwt.verify(token, SECRET);
        next();
    } catch {
        res.sendStatus(403);
    }
}

app.post("/books/review/:isbn", auth, (req, res) => {
    const book = books.find(b => b.isbn === req.params.isbn);
    if (book) {
        book.reviews.push(req.body.review);
        res.json("Review added");
    }
});

app.delete("/books/review/:isbn", auth, (req, res) => {
    const book = books.find(b => b.isbn === req.params.isbn);
    if (book) {
        book.reviews = [];
        res.json("Review deleted");
    }
});

app.listen(3000, () => console.log("Server running"));