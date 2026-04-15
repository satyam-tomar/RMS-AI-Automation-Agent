class ExpressError extends Error {
    constructor(statusCode, message) {
        super(message); // ← was super() which left message unset on Error base
        this.statusCode = statusCode;
        this.message = message;
    }
}

module.exports = ExpressError;