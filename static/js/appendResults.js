const form = document.querySelector('#form')
form.addEventListener('onsubmit', event => {
	event.preventDefault()

	form.reset()

	const resultsDiv = document.querySelector('#results')
	resultsDiv.style.display = 'block'
})

const body = document.body
body.addEventListener('onload', () => {
	const resultsDiv = document.querySelector('#results')
	resultsDiv.style.display = 'none'
})