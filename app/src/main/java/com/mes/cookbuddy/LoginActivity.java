package com.mes.cookbuddy;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.os.StrictMode;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

public class LoginActivity extends AppCompatActivity implements View.OnClickListener{

    Button bttn_login,bttn_sign;
    EditText log_et_username,log_et_password;
    TextView log_txt_verify,log_txt_or;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
        bttn_sign=(Button)findViewById(R.id.bttn_sign);
        bttn_login=(Button) findViewById(R.id.bttn_login);
        log_et_username=(EditText) findViewById(R.id.log_et_username);
        log_et_password=(EditText) findViewById(R.id.log_et_password);
        log_txt_verify=(TextView) findViewById(R.id.log_txt_verify);
        log_txt_or=(TextView) findViewById(R.id.log_txt_or);

        // security
        int SDK_INT = android.os.Build.VERSION.SDK_INT;
        if (SDK_INT > 8){
            StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
            StrictMode.setThreadPolicy(policy);
        }

        bttn_login.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                try {
                    DataBase db=new DataBase();
                    if(db.userinfoCheck(log_et_username.getText().toString(),log_et_password.getText().toString())){
                        Intent loginToHome = new Intent(LoginActivity.this,HomePageActivity.class);
                        loginToHome.putExtra("log_et_username",log_et_username.getText().toString());
                        startActivity(loginToHome);
                    }
                    else{
                        log_txt_verify.setVisibility(View.VISIBLE);
                        log_txt_or.setVisibility(View.VISIBLE);
                    }
                }catch (Exception ee){
                    ee.printStackTrace();
                }
            }
        });
        bttn_sign.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent LoginToSign = new Intent(LoginActivity.this,SignUpActivity.class);
                startActivity(LoginToSign);
            }
        });


    }

    @Override
    public void onClick(View v) {

    }
}