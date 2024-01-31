package com.mes.cookbuddy;

import android.os.StrictMode;
import android.provider.ContactsContract;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.Statement;

public class DataBase {
    private Connection conn;

    public DataBase() {
        int SDK_INT = android.os.Build.VERSION.SDK_INT;
        if (SDK_INT > 8){
            StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
            StrictMode.setThreadPolicy(policy);
        }
        conn=connect();
    }
    public Connection connect() {
        try {
            Class dbDriver = Class.forName("org.postgresql.Driver");
            String jdbcURL = "jdbc:postgresql://10.0.2.2:5432/postgres";
            conn = DriverManager.getConnection(jdbcURL, "postgres", "melin123");
        } catch (Exception e) {
            e.printStackTrace();
        }
        return conn;
    }
  //----Show user info
    public UserInfoForLogin userinfoView(String name) {
        UserInfoForLogin ui=new UserInfoForLogin();
        try {
            Statement statement = conn.createStatement();
            ResultSet rs = statement.executeQuery("SELECT * FROM  public.userinfo dn WHERE dn.username='" + name + "' ORDER BY dn.id;");
            while (rs.next()) {
                ui.setId(rs.getInt("id"));
                ui.setUsername(rs.getString("username"));
                ui.setFirstname(rs.getString("firstname"));
                ui.setLastname(rs.getString("lastname"));
                ui.setEmail(rs.getString("email"));
                ui.setPassword(rs.getString("password"));
                ui.setAge(rs.getInt("ages"));
                //System.out.println("ID = " + rs.getInt("id") + " USERNAME = " + rs.getString("username") + " MAIL = " + rs.getString("email")+ " AGE = " + rs.getInt("ages")+" fistname = "+ rs.getString("firstname")+" lastname = "+ rs.getString("lastname"));
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return ui;
    }
    //----Checks if username and password match.
    public boolean userinfoCheck(String username,String password) {
        try {
            Statement statement = conn.createStatement();
            ResultSet rs = statement.executeQuery("SELECT * FROM  public.userinfo dn WHERE dn.username='" + username + "' ORDER BY dn.id;");
            while (rs.next()) {
                if(!rs.getString("username").isEmpty()&&rs.getString("password").equals(password)){
                    return true;
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return false;
    }
    //---- Check Username is unique or not
    public boolean userUsernameCheck(String username) {
        try {
            Statement statement = conn.createStatement();
            ResultSet rs = statement.executeQuery("SELECT * FROM  public.userinfo dn WHERE dn.username='" + username + "' ORDER BY dn.id;");
            int count=0;
            while (rs.next()) {
                count++;
            }
            if(count==0){
                return true;
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return false;
    }
    //---- Add database new user
    public void userinfoInsert(UserInfoForLogin ui) {
        try {
            String SQL = "INSERT INTO public.userinfo(username, email, ages, firstname, lastname, password) VALUES(?, ?, ?, ?, ?, ?); ";
            PreparedStatement prp = conn.prepareStatement(SQL);
            prp.setString(1, ui.getUsername());
            prp.setString(2, ui.getEmail());
            prp.setInt(3, ui.getAge());
            prp.setString(4,ui.getFirstname());
            prp.setString(5,ui.getLastname());
            prp.setString(6,ui.getPassword());
            int row = prp.executeUpdate();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
//---- Update data in database
    public void userinfoUpdate(UserInfoForLogin ui) {
        try {
            String SQL = "UPDATE public.userinfo SET username=?, email=?, ages=?, firstname=?, lastname=?, password=? WHERE username='" + ui.getUsername() + "'; ";
            PreparedStatement prp = conn.prepareStatement(SQL);
            prp.setString(1, ui.getUsername());
            prp.setString(2, ui.getEmail());
            prp.setInt(3, ui.getAge());
            prp.setString(4,ui.getFirstname());
            prp.setString(5,ui.getLastname());
            prp.setString(6, ui.getPassword());
            int row = prp.executeUpdate();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void userinfoDelete(String user) {
        try {
            String SQL = "DELETE FROM public.userinfo WHERE username='" + user + "'; ";
            PreparedStatement prp = conn.prepareStatement(SQL);
            prp.executeUpdate();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
