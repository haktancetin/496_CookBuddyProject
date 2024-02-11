package com.cookbuddy.modal;

import java.io.Serializable;
import javax.faces.bean.ManagedBean;
import javax.faces.bean.SessionScoped;
import org.springframework.beans.factory.annotation.Autowired;
import com.cookbuddy.data.Database;
import javax.annotation.PostConstruct;
import javax.faces.application.FacesMessage;
import javax.faces.context.FacesContext;
import org.springframework.stereotype.Component;

@Component
@SessionScoped
@ManagedBean(name = "signup")

public class Signup implements Serializable {
  
   
    @Autowired
    private Database database;

    private Signup sgn;

    private String username;
    private String firstname;
    private String lastname;
    private int ages;
    private String email;
    private String password;
    private String verifypassword;

    @PostConstruct
	public void init() {
            sgn=new Signup();
        }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getFirstname() {
        return firstname;
    }

    public void setFirstname(String firstname) {
        this.firstname = firstname;
    }

    public String getLastname() {
        return lastname;
    }

    public void setLastname(String lastname) {
        this.lastname = lastname;
    }

    public int getAges() {
        return ages;
    }

    public void setAges(int ages) {
        this.ages = ages;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public String getVerifypassword() {
        return verifypassword;
    }

    public void setVerifypassword(String verifypassword) {
        this.verifypassword = verifypassword;
    }
    
 

    public Signup getSgn() {
        return sgn;
    }

    public void setSgn(Signup sgn) {
        this.sgn = sgn;
    }

    @Override
    public String toString() {
        return "Signup{" + "sgn=" + sgn + ", username=" + username + ", firstname=" + firstname + ", lastname=" + lastname + ", ages=" + ages + ", email=" + email + ", password=" + password + ", verifypassword=" + verifypassword + '}';
    }
    
    


    public String kontrol() {
        Login lgn = database.loginAl(username, password);
        String rtn = "signup.xhtml";
        
        return rtn;
    }
    public String saveProfile() {
        String message="";
        int control=0;
        
        if(sgn.username.isEmpty()){
            FacesContext.getCurrentInstance().addMessage(null, new FacesMessage(FacesMessage.SEVERITY_WARN, "Username can not empty.", ""));
            control=1;
        }
        System.out.println("username========"+sgn.username);
        if(sgn.firstname.isEmpty()){
            FacesContext.getCurrentInstance().addMessage(null, new FacesMessage(FacesMessage.SEVERITY_WARN, "Fistname can not empty.", ""));
            control=1;
        }
        if(sgn.lastname.isEmpty()){
            FacesContext.getCurrentInstance().addMessage(null, new FacesMessage(FacesMessage.SEVERITY_WARN, "Lastname can not empty.", ""));
            control=1;
        }
        if(sgn.ages==0){
            FacesContext.getCurrentInstance().addMessage(null, new FacesMessage(FacesMessage.SEVERITY_WARN, "Ages can not empty.", ""));
            control=1;
        }
        if(sgn.email.isEmpty()){
            FacesContext.getCurrentInstance().addMessage(null, new FacesMessage(FacesMessage.SEVERITY_WARN, "E-mail can not empty.", ""));
            control=1;
        }
        if(sgn.password.isEmpty()){
            FacesContext.getCurrentInstance().addMessage(null, new FacesMessage(FacesMessage.SEVERITY_WARN, "Password can not empty.", ""));
            control=1;
        }
        if(sgn.verifypassword.isEmpty()){
            FacesContext.getCurrentInstance().addMessage(null, new FacesMessage(FacesMessage.SEVERITY_WARN, "Password verify can not empty.", ""));
            control=1;
        }
        Signup signup=database.signAl(sgn.username);
        if(signup.username.equals(sgn.username)) {
        	FacesContext.getCurrentInstance().addMessage(null, new FacesMessage(FacesMessage.SEVERITY_WARN, "Username is used.", ""));
            control=1;
        }
       if(control!=1){
            database.profilEkle(sgn);
        }
        String rtn = "";
            
        return rtn;
    }
}
