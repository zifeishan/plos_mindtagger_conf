COPY (
    SELECT m.doc_id
         , m.relation_id
         , m.sent_id_1
         , m.sent_id_2
         , m.is_correct
         , m.expectation
         , s1.words as s1_words
         , s2.words as s2_words
         , m.words_1 as m1_words
         , m.words_2 as m2_words
         , m.wordidxs_1
         , m.wordidxs_2
         , m.wordidxs_1[1] as m1_start
         , (select max(x) from unnest(m.wordidxs_1) x) as m1_end
         , m.wordidxs_2[1] as m2_start
         , (select max(x) from unnest(m.wordidxs_2) x) as m2_end
      FROM gene_hpoterm_relations_is_correct_inference m
         , sentences s1
         , sentences s2
     WHERE s1.sent_id = m.sent_id_1
       AND s2.sent_id = m.sent_id_2
       AND s1.doc_id = m.doc_id
       AND s2.doc_id = m.doc_id
       AND expectation > 0.9
     GROUP BY m.doc_id
            , m.relation_id
            , m.sent_id_1
            , m.sent_id_2
            , m.is_correct
            , m.expectation
            , s1.words
            , s2.words
            , m.words_1
            , m.words_2
            , m.wordidxs_1
            , m.wordidxs_2
  ORDER BY random()
) TO STDOUT WITH CSV HEADER;


