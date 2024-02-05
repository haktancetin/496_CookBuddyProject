package com.mes.cookbuddy;

import androidx.annotation.NonNull;
import androidx.appcompat.app.ActionBarDrawerToggle;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.view.GravityCompat;
import androidx.drawerlayout.widget.DrawerLayout;

import android.content.Intent;
import android.os.Bundle;
import android.provider.MediaStore;
import android.view.MenuItem;
import android.view.View;
import android.widget.RelativeLayout;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.widget.Toolbar;


import com.google.android.material.bottomappbar.BottomAppBar;
import com.google.android.material.bottomnavigation.BottomNavigationView;
import com.google.android.material.navigation.NavigationBarView;
import com.google.android.material.navigation.NavigationView;

public class HomePageActivity extends AppCompatActivity {

    DrawerLayout homeDrawerLayout;
    NavigationView home_navigationView;

    Toolbar home_toolbar;
    TextView home_txt_user;
    BottomNavigationView home_bottomnav;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_home_page);

        homeDrawerLayout=(DrawerLayout) findViewById(R.id.home_drawer);
        home_navigationView=(NavigationView) findViewById(R.id.home_navView);
        home_toolbar=(Toolbar) findViewById(R.id.home_toolbar);
        View headerView = home_navigationView.getHeaderView(0);
        home_txt_user=(TextView) headerView.findViewById(R.id.home_txt_user);
        home_bottomnav=(BottomNavigationView)findViewById(R.id.home_bottomnav);



        Intent logHomeInt=getIntent();
        String log_userName=logHomeInt.getStringExtra("log_et_username");
        home_txt_user.setText(log_userName);


        ActionBarDrawerToggle toggle=new ActionBarDrawerToggle(this,homeDrawerLayout,home_toolbar,R.string.open,R.string.close);
        homeDrawerLayout.addDrawerListener(toggle);
        toggle.syncState();
        toggle.getDrawerArrowDrawable().setColor(getResources().getColor(R.color.black));


        home_navigationView.setNavigationItemSelectedListener(new NavigationView.OnNavigationItemSelectedListener() {

            @Override
            public boolean onNavigationItemSelected(@NonNull MenuItem item) {
                if(item.getItemId()==R.id.logout){
                    Intent HomeToLogout = new Intent(HomePageActivity.this,LoginActivity.class);
                    startActivity(HomeToLogout);
                }
                if(item.getItemId()==R.id.account){
                    Intent account = new Intent(HomePageActivity.this,ProfileActivity.class);
                    account.putExtra("log_et_username",log_userName);
                    startActivity(account);
                }

                return false;
            }

        });
        home_bottomnav.setOnItemSelectedListener(new NavigationBarView.OnItemSelectedListener() {
            @Override
            public boolean onNavigationItemSelected(@NonNull MenuItem item) {
                if(item.getItemId()==R.id.bottom_home){
                    Intent camera = new Intent(HomePageActivity.this,HomePageActivity.class);
                    startActivity(camera);
                }
                if(item.getItemId()==R.id.camera){
                    Intent camera = new Intent(HomePageActivity.this,CameraActivity.class);
                    startActivity(camera);
                }
                return false;
            }
        });



    }

}