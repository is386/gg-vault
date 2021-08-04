let games_url = "http://127.0.0.1:8080/games"

function loadGames() {
    $.ajax({
        url: games_url,
        type: 'POST',
        dataType: 'json',
        headers: {"Authorization": "Bearer " + localStorage.ggToken},
        complete: function(data) {
            let status = data.status;
            if (status == 200) {
                populate(data.responseJSON);
            }
        }
    });
}

function populate(games) {
    populateTable(games.my_games, $("#my-games-tbody"));
    populateTable(games.wishlist, $("#wishlist-tbody"));
}

function populateTable(games, tbody) {
    for (let g of games) {
        let tr = $("<tr></tr>").attr({"id": g.id});
        tr.append($("<td></td>").append($("<img>").attr({"src": g.cover})))
        tr.append($("<td></td>").text(g.name));
        tr.append($("<td></td>").text(g.genre));
        tr.append($("<td></td>").append($("<button></button>").addClass("trash-btn").append($("<i></i>").addClass("fa fa-trash"))));
        tbody.append(tr);
    }
}

function deleteGame(gameId) {

}