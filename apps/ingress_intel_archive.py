# 해시 체크를 사용해서 인텔맵이 5초전의 인텔맵과 같다면, 로딩이 끝난 것 간주하는 코드
#                log_or_print(loading_msg.get_attribute('style'))
#                first_hash = hash(driver.page_source)
#                log_or_print('first hash : %s' % first_hash)
#                time.sleep(10)
#                second_hash = hash(driver.page_source)
#                log_or_print('second hash : %s' % second_hash)
#                if second_hash == first_hash:
#                    time.sleep(5)
#                    third_hash = hash(driver.page_source)
#                    log_or_print('third hash : %s' % third_hash)
#                    if second_hash == third_hash:
#                        attachments_dict['color'] = GREEN
#                        log_or_print('5초뒤에도 같은화면')
#                   log_or_print('style이 none이었다고함')
#                   first_check = True
#                    time.sleep(3)
#                   if loading_msg.get_attribute('style') == 'display: none;':
#                       log_or_print('더블체크도 성공했다고함')
#                        second_check = True
#                       break
#                    else:
#                        first_check = False
#                time.sleep(3)
