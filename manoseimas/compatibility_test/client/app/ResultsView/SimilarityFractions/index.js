import React from 'react'
import { SimilarityBar } from '../../../components'
import styles from '../../../styles/views/results.css'

function calculate_similarity (user_answers, fraction_answers) {
    let points = 0,
        answers_count = 0

    for (let answer_id in fraction_answers) {
        if (user_answers[answer_id]) {
            answers_count++
            points += Math.abs((user_answers[answer_id] + fraction_answers[answer_id]) / 2)
        }
    }

    return Math.round((points / answers_count)*100)
}

function getAnswer (answer) {
    answer = (answer) ? answer.toString() : '0'
    switch (answer) {
        case '1':
            return 'taip'
        case '-1':
            return 'ne'
        default:
            return 'praleista'
    }
}

const SimilarityFractions = ({user_answers, fractions, topics}) =>
    <div>
        <div className={styles.note}>
            Kuo didesnis procentas, tuo labiau frakcija atitinka Jūsų pažiūras.
        </div>
        {fractions.map(fraction => {
            let similarity = calculate_similarity(user_answers, fraction.answers)
            return (
                <div className={styles.item} key={fraction.short_title}>
                    <div className={styles.img}>
                        <img src={fraction.logo} alt={fraction.title + ' logo'} />
                    </div>
                    <main>
                        <div className={styles.title}>{fraction.title}, {similarity}%</div>
                        <SimilarityBar similarity={similarity} />
                        <a href={'#' + fraction.short_title}>
                            {fraction.members_amount} nariai {' '}
                            <div className={styles.arrow}></div>
                        </a>
                    </main>
                </div>
            )
        })}
        <div className={styles.topics}>
            <h3>Interaktyvūs frakcijų rezultatai pagal klausimus</h3>
            <div className={styles.note}>
                Šioje rezultatų dalyje galite keisti savo atsakymus ir stebėti kaip keičiasi rezultatai.
            </div>
            <ol>
                {topics.map(topic => {
                    return <li key={topic.id}>
                        {topic.name} - {getAnswer(user_answers[topic.id])} <br />
                        <label><input type='checkbox' name={'topic'+topic.id} value={topic.id} />
                        šis klausimas man svarbus</label>
                        <div className={styles['similarity-bar']}>
                            <div className={styles.no}>PRIEŠ</div>
                            <div style={{width: '500px'}}>
                                <div className={styles.line}></div>
                                <div className={styles.actions}>
                                    <div className={styles.action}>
                                        <img src={(user_answers[topic.id] === -1) ? '/static/img/person-active.png' : '/static/img/person.png'}
                                             onClick={() => console.log('NO')} />
                                    </div>
                                    <div className={styles.action}>
                                        <img src={(user_answers[topic.id] === undefined) ? '/static/img/person-active.png' : '/static/img/person.png'}
                                             onClick={() => console.log('SKIP')} />
                                    </div>
                                    <div className={styles.action}>
                                        <img src={(user_answers[topic.id]) ? '/static/img/person-active.png' : '/static/img/person.png'}
                                             onClick={() => console.log('YES')} />
                                    </div>
                                </div>
                            </div>
                            <div className={styles.yes}>UŽ</div>
                        </div>
                    </li>
                })}
            </ol>
        </div>
    </div>


SimilarityFractions.propTypes = {
  user_answers: React.PropTypes.object,
  fractions: React.PropTypes.array,
  topics: React.PropTypes.array
}

export default SimilarityFractions