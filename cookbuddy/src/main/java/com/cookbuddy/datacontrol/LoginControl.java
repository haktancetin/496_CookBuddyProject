/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.cookbuddy.datacontrol;

import com.cookbuddy.modal.Login;
import javax.faces.bean.ManagedBean;

import javax.faces.bean.ViewScoped;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import com.cookbuddy.data.Database;

/**
 *
 * @author Melin
 */
@ManagedBean(name = "loginControl")
@ViewScoped
public class LoginControl {
    @Autowired
    private Database database;
    
    public void control(){
        Login lgn=database.loginAl("username","password");
        System.out.println("LoginControl: "+lgn);
    }
}
