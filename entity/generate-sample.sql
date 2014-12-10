COPY (
    SELECT m.mention_id
         , s.sent_id
         , m.is_correct
         , m.expectation
         , s.words as s_words
         , m.words as m_words
	 --, m.wordidxs as mention_pos
         , m.wordidxs[1] as m_start
         , (select max(x) from unnest(m.wordidxs) x) as m_end
      FROM gene_mentions_is_correct_inference m
         , sentences s
     WHERE s.sent_id = m.sent_id
       AND s.doc_id = m.doc_id
       AND expectation > 0.9
  ORDER BY random()
) TO STDOUT WITH CSV HEADER;

