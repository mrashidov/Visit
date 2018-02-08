function hide_subcat(id) {
	var cards,card_deck,checked,hidden_cat;
	card_deck = document.getElementById('places-cards');
	cards = card_deck.getElementsByClassName('place-card');
	for (var i = 0; i < cards.length; i++) {
		hidden_cat = cards[i].getElementsByTagName('input')[0];
		checked = document.getElementById('subcat'+id).checked;
		if (checked){
			if(hidden_cat.value!=id){
				cards[i].style.display='none';
			}
		}else{
			if(hidden_cat.value!=id){
				cards[i].style.display='block';
			}

		}
	}
}
