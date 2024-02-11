package com.cookbuddy.data;

import com.cookbuddy.modal.Login;
import com.cookbuddy.modal.Signup;


public interface Database {

    Login loginAl(String username,String password);
    Signup signAl(String username);
    int profilEkle(Signup sign);
    
}
