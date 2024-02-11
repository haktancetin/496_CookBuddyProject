package com.cookbuddy.modal;

import java.io.Serializable;
import javax.faces.bean.ManagedBean;
import javax.faces.bean.SessionScoped;
import org.springframework.beans.factory.annotation.Autowired;
import com.cookbuddy.data.Database;
import javax.faces.application.FacesMessage;
import javax.faces.context.FacesContext;
import org.springframework.stereotype.Component;

@Component
@SessionScoped
@ManagedBean(name = "login")

public class Login implements Serializable {
  
   
    @Autowired
    private Database database;

    

    private String username;
    private String password;

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    @Override
    public String toString() {
        return "Login{" + "username=" + username + ", password=" + password + '}';
    }

    public String kontrol() {
        Login lgn = database.loginAl(username, password);
        String rtn = "login";
        if (lgn.getUsername().equals(username) & lgn.getPassword().equals(password)) {
            //FacesContext.getCurrentInstance().addMessage(null, new FacesMessage(FacesMessage.SEVERITY_WARN, "Bilgiler Doğru", "Sayfaya Yönlendiriliyor"));
            rtn = "home.xhtml";
        } else {
            FacesContext.getCurrentInstance().addMessage(null, new FacesMessage(FacesMessage.SEVERITY_FATAL, "Check your username and password", "Doğru Kullanıcı Adı ve Şifre ile Deneyin."));
        }
        return rtn;
    }
    public String profilkaydet() {
        //Login lgn = database.profilEkle(username, password);
        String rtn = "";
            FacesContext.getCurrentInstance().addMessage(null, new FacesMessage(FacesMessage.SEVERITY_WARN, "Saved profile", "Kaydedildi"));
        return rtn;
    }
}
