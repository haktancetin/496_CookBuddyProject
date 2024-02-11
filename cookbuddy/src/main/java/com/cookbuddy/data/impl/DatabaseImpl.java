package com.cookbuddy.data.impl;

import com.cookbuddy.modal.Login;
import java.util.HashMap;
import java.util.Map;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.BeanPropertyRowMapper;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;
import com.cookbuddy.data.Database;
import com.cookbuddy.modal.Signup;
import java.util.List;
import javax.faces.application.FacesMessage;
import javax.faces.context.FacesContext;
import org.springframework.jdbc.core.namedparam.MapSqlParameterSource;
import org.springframework.jdbc.core.namedparam.SqlParameterSource;
import org.springframework.jdbc.support.GeneratedKeyHolder;

@Service
public class DatabaseImpl implements Database {

    @Autowired
    private JdbcTemplate jdbcTemplate;

    @Autowired
    private NamedParameterJdbcTemplate namedParameterJdbcTemplate;

    public static final String DEFAULT_SCHEMA = "public";

    @Transactional(propagation = Propagation.REQUIRED)
    @Override
    public Login loginAl(String username, String password) {
        StringBuilder buffer = new StringBuilder();
        buffer.append("SELECT t.username,t.password FROM " + DEFAULT_SCHEMA + ".userinfo t ");
        buffer.append("WHERE (t.username = :username);");
        Map<String, Object> params = new HashMap<>();
        params.put("username", username);

        List<Login> rtnxList = namedParameterJdbcTemplate.query(buffer.toString(), params, BeanPropertyRowMapper.newInstance(Login.class));
        Login rtnx = null;
        if (rtnxList != null) {
            rtnx = rtnxList.get(0);
        }
        return rtnx;
    }

    @Transactional(propagation = Propagation.REQUIRED)
    @Override
    public Signup signAl(String username) {
        StringBuilder buffer = new StringBuilder();
        buffer.append("SELECT t.username,t.password FROM " + DEFAULT_SCHEMA + ".userinfo t ");
        buffer.append("WHERE (t.username = :username);");
        Map<String, Object> params = new HashMap<>();
        params.put("username", username);

        List<Signup> rtnxList = namedParameterJdbcTemplate.query(buffer.toString(), params, BeanPropertyRowMapper.newInstance(Signup.class));
        Signup rtnx = null;
        if (rtnxList != null) {
        	if(rtnxList.size()>0)
            rtnx = rtnxList.get(0);
        }
        return rtnx;
    }

    @Transactional(propagation = Propagation.REQUIRED)
    @Override
    public int profilEkle(Signup sign) {
        String sql = "INSERT INTO " + DEFAULT_SCHEMA + ".userinfo (username,firstname,lastname,ages,email,password) VALUES (:username,:firstname,:lastname,:ages,:email,:password); ";
        SqlParameterSource paramSource = new MapSqlParameterSource()
                .addValue("username", sign.getUsername()).addValue("firstname", sign.getFirstname())
                .addValue("lastname", sign.getLastname()).addValue("ages", sign.getAges()).addValue("email", sign.getEmail()).addValue("password", sign.getPassword());
        namedParameterJdbcTemplate.update(sql, paramSource);
        //FacesContext.getCurrentInstance().addMessage(null, new FacesMessage(FacesMessage.SEVERITY_INFO, "Bilgiler Kaydedildi", "Bilgiler Kaydedildi..."));
        return 0;
    }

}
