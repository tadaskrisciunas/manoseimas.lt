function(doc) {
    if (doc.doc_type == 'Voting' && doc.votes) {
        for(var i = 0; i < doc.votes.aye.length; i++) {
            emit([doc.votes.aye[i][0], doc.created], {'aye': 1});
        }

        for(var i = 0; i < doc.votes.no.length; i++) {
            emit([doc.votes.no[i][0], doc.created], {'no': 1});
        }

        for(var i = 0; i < doc.votes.abstain.length; i++) {
            emit([doc.votes.abstain[i][0], doc.created], {'abstain': 1});
        }
    }
}
