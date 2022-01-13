accounts/ signup/ [name='account_signup']                                done
accounts/ login/ [name='account_login']                                  done
accounts/ logout/ [name='account_logout']                                 done
accounts/ password/change/ [name='account_change_password']                 done
accounts/ password/set/ [name='account_set_password']                       done
accounts/ inactive/ [name='account_inactive']                               done
accounts/ email/ [name='account_email']                                     done
accounts/ confirm-email/ [name='account_email_verification_sent']           done
accounts/ ^confirm-email/(?P<key>[-:\w]+)/$ [name='account_confirm_email']  done
accounts/ password/reset/ [name='account_reset_password']                   done
accounts/ password/reset/done/ [name='account_reset_password_done']         done
accounts/ ^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$ [name='account_reset_password_from_key']  done
accounts/ password/reset/key/done/ [name='account_reset_password_from_key_done']        done


