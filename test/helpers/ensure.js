const { expect } = require('chai')

function ensure(actual, expected) {
    const newActual = (typeof actual == 'function')? actual() : actual
    const newExptected = expected === undefined ? true : expected

    expect(newActual).to.equal(newExptected)
}

module.exports = { ensure }
