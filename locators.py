class SiteLocators:
    POST_COUNTER = 'div.profileStats_number.profileTabAnswerCount'
    LIKES_COUNTER = 'div.profileStats_number.profileTabLikeCount'
    QUESTIONS = 'article.item.streamItem.streamItem-answer'
    NEXT = 'a.item-page-next'


class PostLocator:
    question = 'header.streamItem_header h2'
    link = 'div.streamItem_properties div.streamItem_details a'
    date = 'div.streamItem_properties div.streamItem_details a time'
    answer = 'div.streamItem_content'
    likes = 'div.streamItem_footer div.heartButton a.counter'
    img = 'div.streamItem_visual a picture source'
    asker_url = 'header.streamItem_header a author'
