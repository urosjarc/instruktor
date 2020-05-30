import {Component, OnInit} from '@angular/core';
import {User} from '../user';
import {UserLoginService} from '../user-login.service';
import {Router, ActivatedRoute} from '@angular/router';

@Component({
  selector: 'app-user-signin',
  templateUrl: './user-signin.component.html',
  styleUrls: ['./user-signin.component.css']
})
export class UserSigninComponent implements OnInit {
  user: User = {username: '', password: '', _id: '', email: ''};

  constructor(private userLoginService: UserLoginService, private route: ActivatedRoute, private router: Router) {
  }

  trySignIn(): void {
    this.userLoginService.signin(this.user).subscribe(user => {
        this.route.queryParams.subscribe(
          params => {
            this.router.navigate([params['returnUrl'] || 'photos']);
          });
      }
    );
  }

  ngOnInit() {
  }

}
