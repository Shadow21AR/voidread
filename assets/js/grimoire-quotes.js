// Grimoire Quote Functionality

document.addEventListener('DOMContentLoaded', function () {
    const quotes = [
        `Every system is a reflection of its creator's assumptions. Break those, and you break the system.`,
        `Obscurity is a veil; knowledge is the blade that parts it.`,
        `To navigate the unknown, first embrace that you know nothing.`,
        `There are no unbreakable systems—only time, pressure, and perspective.`,
        `The key was always there. You just hadn't asked the right question.`,
        `Every anomaly is a door. Most just don't see it.`,
        `Beneath every layer of protection lies trust. And trust can be manipulated.`,
        `The moment you think you've understood everything is the moment you're most vulnerable.`,
        `Patterns are the fingerprints of truth in chaos.`,
        `No god guards the gates. Only misdirection, delay, and entropy.`,
        `The path is hidden not by complexity, but by convention.`,
        `A closed system is just a mind that hasn't been challenged.`,
        `The system reveals itself to those who observe, not rush.`,
        `In every protocol lies a ritual. In every exploit, a revelation.`,
        `You do not break in. You are allowed in—by oversight, by arrogance, or by time.`,
        `Nothing is secure. Only less known.`,
        `There are no secrets, only delays in discovery.`,
        `Information flows where resistance is weakest. So do intrusions.`,
        `The veil doesn't protect—it tempts the curious.`,
        `True power lies not in access, but in remaining unseen after it.`
    ];

    const quoteElement = document.getElementById("quote");
    if (quoteElement) {
        const randomQuote = quotes[Math.floor(Math.random() * quotes.length)];
        quoteElement.innerText = randomQuote;
    }
});
