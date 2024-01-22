package com.mes.cookbuddy;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {

    TextView tvGetStart;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        tvGetStart=(TextView)findViewById(R.id.tvGetStart);
        tvGetStart.setOnClickListener(this::onClick);
    }
    public void onClick(View v){
        Intent MainMenuToLogin = new Intent(MainActivity.this,LoginActivity.class);
        startActivity(MainMenuToLogin);
    }
}