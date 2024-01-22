package com.mes.cookbuddy;

import android.os.StrictMode;

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

    public void userinfoView(String name) {
        try {
            Statement statement = conn.createStatement();
            ResultSet rs = statement.executeQuery("SELECT * FROM  public.userinfo dn WHERE dn.username='" + name + "' ORDER BY dn.id;");
            while (rs.next()) {
                System.out.println("ID = " + rs.getInt("id") + " USERNAME = " + rs.getString("username") + " MAIL = " + rs.getString("mail")+ " AGE = " + rs.getInt("ages")+" fistname = "+ rs.getString("firstname")+" lastname = "+ rs.getString("lastname"));
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
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
    public boolean userUsernameCheck(String username) {
        try {
            Statement statement = conn.createStatement();
            ResultSet rs = statement.executeQuery("SELECT * FROM  public.userinfo dn WHERE dn.username='" + username + "' ORDER BY dn.id;");
            int count=0;
            while (rs.next()) {
                count++;
                if(count==0){
                    return true;
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return false;
    }
    public void userinfoInsert(String username,String mail,int age,String firstname,String lastname,String password) {
        try {
            String SQL = "INSERT INTO public.userinfo(username, mail, ages, firstname, lastname, password) VALUES(?, ?, ?, ?, ?, ?); ";
            PreparedStatement prp = conn.prepareStatement(SQL);
            prp.setString(1, username);
            prp.setString(2, mail);
            prp.setInt(3, age);
            prp.setString(4,firstname);
            prp.setString(5,lastname);
            prp.setString(6,password);
            int row = prp.executeUpdate();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void userinfoUpdate(String user) {
        try {
            String SQL = "UPDATE public.userinfo SET username=?, mail=?, ages=? WHERE username='" + user + "'; ";
            PreparedStatement prp = conn.prepareStatement(SQL);
            //int row = prp.executeUpdate();
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
